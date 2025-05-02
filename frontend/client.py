import grpc
import base64
from PIL import Image, ImageDraw
from io import BytesIO
import text2image_pb2
import text2image_pb2_grpc
import gradio as gr
import grpc.aio
import asyncio

# === Embedded CSS ===
custom_css = """
/* Your previous CSS with adjustments for the layout */
body {
    font-family: 'Arial', sans-serif;
    background-color: black;
    margin: 0;
    padding: 40px;
    background-size: cover;
    background-position: center;
}
.gradio-container {
    background-color: #fefae0;
    color: #283618;
    border-radius: 10px;
    padding: 40px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    max-width: 1200px;  /* Increased width */
    margin: auto;
    text-align: center;
    display: flex;
    justify-content: center;
    align-items: center;
}

h1 {
    font-size: 2.5em;
    color: #283618;
    margin-bottom: 30px;
    font-weight: 600;
    text-transform: uppercase;
}
input, button {
    padding: 15px;
    margin: 15px 0;
    border-radius: 8px;
    border: 2px solid #ddd;
    width: 100%;
    font-size: 16px;
    background-color: #fafafa;
    transition: all 0.3s ease;
}
input:focus, button:focus {
    outline: none;
    border-color: #bc6c25;
    box-shadow: 0 0 8px rgba(188, 108, 37, 0.5);
}
button {
    background-color: #606c38;
    color: white;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.2s;
    border: none;
}
button:hover {
    background-color: #283618;
    transform: scale(1.05);
}
button:active {
    transform: scale(0.98);
}
img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    margin-top: 20px;
    border: 2px solid #ddd;
    transition: all 0.3s ease;
}
img:hover {
    transform: scale(1.02);
}
input::placeholder {
    color: #aaa;
    font-style: italic;
}
footer {
    font-size: 14px;
    color: #777;
    margin-top: 40px;
    padding: 10px;
    text-align: center;
    font-weight: 600;
}
/* Hide image label and icon */
.gr-image-label {
    display: none !important;
}

/* Move the image buttons (download, expand) to top-right */
.gr-image-box .image-buttons {
    top: 5px !important;
    right: 5px !important;
    bottom: auto !important;
    position: absolute !important;
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 5px;
    padding: 2px;
    z-index: 10;
}

@media (max-width: 768px) {
    .gradio-container {
        width: 80%;
        padding: 20px;
    }
    h1 {
        font-size: 2em;
    }
}
#loader-frame {
    width: 100%;
    height: 400px;
    border: none;
    display: none;
    margin-bottom: 20px;
}

/* Flexbox layout for input/output boxes */
#input-container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    width: 45%;  /* Initial width */
    transition: 0.5s ease;
}
#output-container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    width: 45%;  /* Initial width */
    transition: 0.5s ease;
    opacity: 0;
    visibility: hidden;
}
#input-left {
    transform: translateX(-100%);  /* Move the input box to the left */
}
#output-right {
    transform: translateX(100%);  /* Move output box to the right */
    opacity: 1;
    visibility: visible;
}
"""

# === gRPC Client Function ===
# Inside generate_image in app_ui.py
async def generate_image(prompt_text, progress=gr.Progress()):
    if not prompt_text.strip():
        raise gr.Error("Prompt cannot be empty. Please enter a valid prompt.")

    print(f"[FRONTEND] Prompt submitted: {prompt_text}")

    total_steps = 20
    for i in range(total_steps):
        await asyncio.sleep(0.05)
        progress(i / total_steps, desc="Generating...")

    try:
        async with grpc.aio.insecure_channel('localhost:50051') as channel:
            stub = text2image_pb2_grpc.Text2ImageServiceStub(channel)
            request = text2image_pb2.TextPrompt(prompt=prompt_text)
            print(f"Sending prompt to server: {prompt_text}")

            response = await stub.GenerateImage(request)

        progress(1.0, desc="Done!")

        img_data = base64.b64decode(response.image_base64)
        image = Image.open(BytesIO(img_data))
        return image

    except grpc.aio.AioRpcError as rpc_error:
        print(f"[FRONTEND ERROR] gRPC Error: {rpc_error.details()}")
        raise gr.Error(f"Server error: {rpc_error.details()}")

    except Exception as e:
        print(f"[FRONTEND ERROR] Unexpected error: {e}")
        raise gr.Error("Something went wrong. Please try again.")


# === Create a simple loading placeholder image ===
def create_placeholder():
    img = Image.new("RGB", (512, 384), color="#ccc")
    d = ImageDraw.Draw(img)
    d.text((180, 180), "Loading...", fill="black")
    return img

loading_placeholder = create_placeholder()

# === Gradio Blocks App ===
with gr.Blocks(css=custom_css) as demo:
    with gr.Row(elem_classes=["gradio-container"]):
        # Define the layout for input and output side by side
        with gr.Column(elem_classes=["gradio-container"]):
            gr.Markdown("# Text-to-Image Generator")
            gr.Markdown("Enter a text prompt to generate an image")

            prompt = gr.Textbox(lines=2, placeholder="Describe your image here...")
            generate_btn = gr.Button("Generate Image")

        with gr.Column(elem_classes=["gradio-container"]):
            image_output = gr.Image(type="pil", label=None, visible=False)
        
        # This wrapper first shows loading, then real image
        async def wrapped_generate(prompt_text, progress=gr.Progress()):
            yield gr.update(value=loading_placeholder, visible=True)  # show loading
            image =await generate_image(prompt_text, progress)
            yield gr.update(value=image, visible=True)  # show final image

        # Button click to initiate image generation and move elements
        def move_layout():
            return [
                gr.update(elem_id="input-container", value="none"),  # Hide input container
                gr.update(elem_id="output-container", visible=True),  # Show output container
                gr.update(value=None, elem_id="input-container", transform="translateX(-100%)"),  # Move left
                gr.update(value=None, elem_id="output-container", transform="translateX(0%)")  # Move right
            ]

        generate_btn.click(
            fn=wrapped_generate,
            inputs=prompt,
            outputs=image_output,
            show_progress=True
        )

demo.launch()
