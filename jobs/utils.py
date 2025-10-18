from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from google import genai
from PIL import Image
from io import BytesIO
import os
from jobs.models import Job

# client = genai.Client()


def generate_content(job_id, prompt=None):
    """
    Generates an image from a prompt and saves it using Django storage.
    Returns the relative URL to the saved image.
    """
    
    prompt = prompt or (
        "A photorealistic close-up portrait of an elderly Japanese ceramicist "
        "with deep, sun-etched wrinkles and a warm, knowing smile..."
    )

    # try:
    #     response = client.models.generate_content(
    #         model="gemini-2.5-flash-image",
    #         contents=prompt,
    #     )
    #     # handle image as before...
    # except Exception as e:
    #     if "RESOURCE_EXHAUSTED" in str(e):
    #         # retry after 60 seconds
    #         print("Rate limit exceeded. Retrying after 60 seconds...")
    #         os.sleep(60)

    # image_parts = [
    #     part.inline_data.data
    #     for part in response.candidates[0].content.parts
    #     if part.inline_data
    # ]

    # if not image_parts:
    #     raise ValueError("No image returned from GenAI model.")

    # image = Image.open(BytesIO(image_parts[0]))

    # # Convert image to bytes
    # buffer = BytesIO()
    # image.save(buffer, format="PNG")
    # buffer.seek(0)

    # # Build a file path using Django storage
    # file_name = f"generated_images/{job_id}.png"
    # saved_path = default_storage.save(file_name, ContentFile(buffer.read()))

    # # Build URL to return to frontend
    # image_url = default_storage.url(saved_path)
    # job = Job.objects.get(id=job_id)
    # job.final_prompt = prompt
    # job.metadata = {"image_url": image_url}
    # job.status = "done"
    # job.save()
    # return image_url
