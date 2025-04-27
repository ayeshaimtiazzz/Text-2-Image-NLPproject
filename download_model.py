from diffusers import StableDiffusionPipeline

# Set Hugging Face cache directory (optional if you already set HF_HOME)
import os
os.environ["HF_HOME"] = "D:/huggingface_cache"

# Download and cache the model
model_id = "stabilityai/sd-turbo"  # (or whatever model you want)
pipe = StableDiffusionPipeline.from_pretrained(model_id)

print("✅ Model downloaded and cached successfully!")
