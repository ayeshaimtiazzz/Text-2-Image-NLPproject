import grpc
import time
import matplotlib.pyplot as plt
import text2image_pb2
import text2image_pb2_grpc

# List of prompts
all_prompts = [
    "a realistic portrait of a cat wearing a royal crown",
    "a 3D render of a futuristic sports car in a cityscape",
    "a group of penguins having a tea party in the snow",
    "a magical owl flying through a glowing cave",
    "a landscape filled with giant floating crystals and waterfalls"
]

def generate_images(prompt_list, stub):
    request = text2image_pb2.TextPrompts(prompts=prompt_list)
    start_time = time.time()
    response = stub.GenerateImages(request)
    end_time = time.time()
    return end_time - start_time

def main():
    server_address = 'localhost:50051'  # Update if needed
    channel = grpc.insecure_channel(server_address)
    stub = text2image_pb2_grpc.Text2ImageServiceStub(channel)

    num_prompts_list = []
    times_taken = []

    for i in range(1, len(all_prompts) + 1):
        subset = all_prompts[:i]
        print(f"Sending {i} prompt(s)...")
        try:
            time_taken = generate_images(subset, stub)
            print(f"Time taken for {i} prompt(s): {time_taken:.2f} seconds")
            num_prompts_list.append(i)
            times_taken.append(time_taken)
        except Exception as e:
            print(f"Error generating {i} prompt(s): {e}")
            num_prompts_list.append(i)
            times_taken.append(None)

    # Plotting the graph
    plt.figure(figsize=(8, 5))
    plt.plot(num_prompts_list, times_taken, marker='o', color='blue', linestyle='-')
    plt.xlabel("Number of Prompts")
    plt.ylabel("Time Taken (seconds)")
    plt.title("Image Generation Time vs Number of Prompts")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("generation_performance.png")
    plt.show()

if __name__ == "__main__":
    main()
