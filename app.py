from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import grpc
import base64

import text2image_pb2, text2image_pb2_grpc

app = FastAPI(title="Text2Image API")

# Define the input request model
class PromptRequest(BaseModel):
    prompt: str

# Define the output response model
class ImageResponse(BaseModel):
    corrected_prompt: str
    image_base64: str

@app.post("/generate", response_model=ImageResponse)
async def generate_image_from_prompt(prompt_request: PromptRequest):
    try:
        # Create an asynchronous gRPC channel
        async with grpc.aio.insecure_channel('localhost:50051') as channel:
            # Create a stub (client) for the Text2ImageService
            stub = text2image_pb2_grpc.Text2ImageServiceStub(channel)
            
            # Create a request object for gRPC
            request = text2image_pb2.TextPrompt(prompt=prompt_request.prompt)
            
            # Call the GenerateImage method from the backend service
            response = await stub.GenerateImage(request)
            
            # Assuming the backend sends a base64 encoded string (make sure this is true)
            image_base64 = response.image_base64  # This should already be base64-encoded
            
            # Ensure the corrected_prompt and image_base64 are returned as a response
            return {
                "corrected_prompt": response.corrected_prompt,
                "image_base64": image_base64
            }

    except grpc.aio.AioRpcError as e:
        # Handle gRPC specific errors
        raise HTTPException(status_code=500, detail=f"gRPC error: {str(e)}")
    except Exception as e:
        # Catch any other errors
        raise HTTPException(status_code=500, detail=str(e))
