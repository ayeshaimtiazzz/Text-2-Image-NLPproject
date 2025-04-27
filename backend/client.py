import grpc
import text2image_pb2
import text2image_pb2_grpc

def run():
    # Create a channel to the server
    channel = grpc.insecure_channel('localhost:50052')
    stub = text2image_pb2_grpc.TextToImageServiceStub(channel)
    
    # Create the TextRequest message with the text and context you want
    text_request = text2image_pb2.TextRequest(
        text="Hello, world!", 
        context="A sunset over the ocean."
    )
    
    # Call the GenerateImage method
    response = stub.GenerateImage(text_request)
    
    print(f"Image URL: {response.image_url}")

if __name__ == '__main__':
    run()
