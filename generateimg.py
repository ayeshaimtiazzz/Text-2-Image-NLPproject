import os
from diffusers import StableDiffusionPipeline

# Set Hugging Face cache directory
os.environ["HF_HOME"] = "D:/huggingface_cache"  # Ensure it points to your cache directory

# Load the model from cache (it will be fetched from D drive if available)
model_id = "stabilityai/sd-turbo"  # Or any other model you used
pipe = StableDiffusionPipeline.from_pretrained(model_id)

# Optionally, set device (GPU/CPU) if needed:
# pipe.to("cuda")  # For GPU, if available
# pipe.to("cpu")  # For CPU

print("Model loaded ✅")

# Take user input for image generation
prompt = input("Enter a prompt for the image: ")

# Generate the image
image = pipe(prompt).images[0]

# Save the generated image
image.save("generated_image.png")

print("Image saved to generated_image.png ✅")
