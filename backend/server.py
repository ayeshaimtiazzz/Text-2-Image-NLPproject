import grpc
from concurrent import futures
import time
import text2image_pb2
import text2image_pb2_grpc

class TextToImageServiceServicer(text2image_pb2_grpc.TextToImageServiceServicer):
    def GenerateImage(self, request, context):
        # Here, the request will be a TextRequest message, so you can access `request.text` and `request.context`
        print(f"Received request: {request.text} with context: {request.context}")
        
        # Here, we simulate generating an image URL
        image_url = f"https://example.com/generated_image?text={request.text}&context={request.context}"

        # Return the response with the generated image URL
        return text2image_pb2.TextResponse(image_url=image_url)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    text2image_pb2_grpc.add_TextToImageServiceServicer_to_server(TextToImageServiceServicer(), server)
    server.add_insecure_port('[::]:50052')
    print("Server started at port 50052...")
    server.start()
    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()


