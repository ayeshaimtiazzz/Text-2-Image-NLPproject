import grpc
import io
import torch
import asyncio
import base64
from PIL import Image, ImageFilter
from textblob import TextBlob

import text2image_pb2
import text2image_pb2_grpc

from diffusers import DiffusionPipeline

class Text2ImageServicer(text2image_pb2_grpc.Text2ImageServiceServicer):
    def __init__(self):
        self.pipe = DiffusionPipeline.from_pretrained(
            "stabilityai/sd-turbo",
            torch_dtype=torch.float32,
            safety_checker=None,
            requires_safety_checker=False
        )
        self.pipe.to("cpu")

    async def GenerateImage(self, request, context):
        try:
            prompt = request.prompt.strip()

            if not prompt:
                raise ValueError("Prompt cannot be empty.")

            corrected_prompt = str(TextBlob(prompt).correct())
            print(f"[SERVER] Corrected prompt: {corrected_prompt}")

            def generate_image():
                with torch.no_grad():
                    image = self.pipe(corrected_prompt, num_inference_steps=5, guidance_scale=5.0).images[0]
                    image = image.resize((384, 384))
                    buffered = io.BytesIO()
                    image.save(buffered, format="PNG")
                    return base64.b64encode(buffered.getvalue()).decode("utf-8")

            image_base64 = await asyncio.to_thread(generate_image)

            return text2image_pb2.ImageResponse(
                corrected_prompt=corrected_prompt,
                image_base64=image_base64
            )

        except ValueError as ve:
            print(f"[SERVER WARNING] {ve}")
            await context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(ve))

        except Exception as e:
            print(f"[SERVER ERROR] {e}")
            await context.abort(grpc.StatusCode.UNKNOWN, f"Server error: {str(e)}")


# Async gRPC server startup
async def serve():
    server = grpc.aio.server()
    text2image_pb2_grpc.add_Text2ImageServiceServicer_to_server(Text2ImageServicer(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    print("Async gRPC server running on port 50051...")
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())
