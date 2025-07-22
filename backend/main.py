import torch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from diffusers import StableDiffusionPipeline
import uuid # Used to create unique filenames

# --- 1. Initialize the FastAPI App ---
app = FastAPI()
# --- ADD THIS CORS MIDDLEWARE SECTION ---
# This allows your frontend (running on any port) to talk to your backend.
origins = ["*"] # For development, allow all origins.

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods
    allow_headers=["*"], # Allow all headers
)

# --- 2. Load the AI Model (ONCE, on startup) ---
# This is crucial for performance. We load the model into memory once when
# the server starts, not every time a request comes in.
print("Loading Stable Diffusion model...")
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")
print("Model loaded and moved to GPU.")

# --- 3. Define the request data structure ---
# This ensures the incoming data has a 'prompt' field of type string.
class ImageRequest(BaseModel):
    prompt: str

# --- 4. Create the API Endpoint ---
@app.post("/api/v1/generate-image")
def generate_image(request: ImageRequest):
    """
    Takes a text prompt and returns a generated image.
    """
    print(f"Received prompt: {request.prompt}")
    
    # Generate a unique filename for each image to prevent overwriting
    unique_filename = f"{uuid.uuid4()}.png"
    
    # Generate the image
    image = pipe(request.prompt).images[0]
    
    # Save the image
    image.save(unique_filename)
    print(f"Image saved as {unique_filename}")
    
    # Return the image file as a response
    return FileResponse(unique_filename, media_type="image/png")

# --- 5. A simple root endpoint to check if the server is running ---
@app.get("/")
def read_root():
    return {"status": "StoryWeaver API is running"}