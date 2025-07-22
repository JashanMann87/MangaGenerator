import torch
from diffusers import StableDiffusionPipeline

print("Libraries imported successfully.")

# Define the model ID. This is a popular and well-supported base model.
model_id = "runwayml/stable-diffusion-v1-5"

# Load the pipeline. 
# We use float16 for better performance and less memory usage on consumer GPUs.
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
print("Pipeline loaded from pre-trained model.")

# Move the model to the GPU for fast inference.
pipe = pipe.to("cuda")
print("Model moved to CUDA (GPU).")

# Define the prompt for your image.
prompt = "A beautiful manga panel of a warrior looking at a futuristic city, high quality, detailed."

# Run the model to generate the image.
print("Generating image from prompt...")
image = pipe(prompt).images[0]
print("Image generated successfully.")

# Save the image to a file in your 'backend' directory.
image.save("test_image.png")
print("Image saved as test_image.png")