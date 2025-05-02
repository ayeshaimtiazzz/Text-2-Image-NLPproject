# Text-2-Image NLP Project

This project combines **Natural Language Processing (NLP)** and **Generative Adversarial Networks (GANs)** to convert text descriptions into images. The goal is to build a pipeline that generates realistic images based on textual prompts using advanced deep learning techniques.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Frontend](#frontend)
- [Backend](#backend)
- [API Documentation](#api-documentation)
- [Running Locally](#running-locally)
- [License](#license)
- [Contributing](#contributing)

## Project Overview

This project leverages the power of **Transformers**, **Stable Diffusion**, and **Deep Learning** techniques to generate high-quality images from text prompts. Users can input any text prompt, and the system will generate an image that matches the description using a **text-to-image** model.

### Core Components:
1. **Frontend**: A web interface built with **Gradio** and **JavaScript**, where users can input text prompts and view the generated images.
2. **Backend**: A server built using **gRPC** and **FastAPI**, handling requests and serving the model that generates images.
3. **Text-to-Image Model**: The **Stable Diffusion** model, specifically the **"stabilityai/sd-turbo"** model, is used for image generation.

## Features

- **Text-to-Image Generation**: Generate images from textual descriptions.
- **Image Download**: Users can download the generated images.
- **Prompt Correction**: Corrects user input text using **TextBlob** to ensure grammatical accuracy before generating images.
- **Scalable Backend**: Designed to handle multiple requests simultaneously.

## Technologies Used

- **Frontend**:
  - [Gradio](https://gradio.app/): For creating the user interface.
  - [JavaScript](https://www.javascript.com/): For handling client-side logic.
  
- **Backend**:
  - [gRPC](https://grpc.io/): For efficient communication between the frontend and backend.
  - [FastAPI](https://fastapi.tiangolo.com/): For handling RESTful API requests.
  - [TextBlob](https://textblob.readthedocs.io/en/dev/): For text correction.
  - [Torch](https://pytorch.org/): For running the **Stable Diffusion** model.
  - **Stable Diffusion** (Model: "stabilityai/sd-turbo"): For text-to-image generation.
  
- **Image Processing**:
  - [PIL (Pillow)](https://pillow.readthedocs.io/en/stable/): For handling image generation and processing.
  
- **Version Control**:
  - [Git](https://git-scm.com/): For version control.
  - [GitHub](https://github.com/): For hosting the repository.

## Installation

Follow these steps to set up the project on your local machine:

1. Clone the repository:
   git clone https://github.com/ayeshaimtiazzz/Text-2-Image-NLPproject.git
   cd Text-2-Image-NLPproject
2.Set up a virtual environment (recommended):
   python3 -m venv venv
   On Windows use `venv\Scripts\activate`
3.Download the pre-trained Stable Diffusion model (optional, can be specified in code if not already included). The model used for image generation is: "stabilityai/sd-turbo": This model is responsible for converting the text prompts into images.
5.Run the server and frontend:
    Backend (gRPC server): Start the server by running:
    python backend/server.py
    Frontend (Web Interface): Run the frontend server with:
    python frontend/client.py
Frontend
The Frontend is built using Gradio and JavaScript. It provides an interface for users to input textual prompts and view the generated images.

Files:
frontend/client.py: The main entry point for running the frontend server.

frontend/generateimagerequest.js: Handles client-side requests to the backend.

frontend/generateimageresponse.js: Processes the response from the server and displays the generated image.

Backend
The Backend consists of an Async gRPC server built using FastAPI and gRPC that handles requests to generate images from text prompts.

Files:
backend/server.py: The gRPC server implementation that serves the text-to-image generation pipeline.

backend/client.py: A legacy client file for communication with the backend, now replaced by the frontend implementation.

API Documentation
gRPC API
The backend server exposes a gRPC API to generate images from text prompts. The API is described as follows:

GenerateImage
Method: POST

Request:

prompt (string): The text description for image generation.

Response:

corrected_prompt (string): The corrected version of the input prompt (using TextBlob).

image_base64 (string): A base64 encoded string representing the generated image in PNG format.

Example gRPC call:
grpcurl -d '{"prompt": "A cat on a mat"}' -plaintext localhost:50051 Text2ImageService.GenerateImage
Running Locally
Run Backend Server:
Navigate to the backend/ directory and run:
python server.py
Run Frontend:
Navigate to the frontend/ directory and run:
python client.py
Access the Application:
Visit http://localhost:5000 in your browser, where you can input text prompts and generate images.


