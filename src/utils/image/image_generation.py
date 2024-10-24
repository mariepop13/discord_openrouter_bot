import replicate
import uuid
from pathlib import Path
import logging
import requests
from config import DEFAULT_IMAGE_GENERATION_MODEL

logger = logging.getLogger(__name__)

async def generate_image(prompt, model=DEFAULT_IMAGE_GENERATION_MODEL, local_filename=None):
    logger.debug(f"Generating image with prompt: {prompt}, model: {model}")
    try:
        output = await replicate.async_run(
            model,
            input={"prompt": prompt}
        )
        logger.debug(f"Raw output for {model}: {output}")
        
        if model == "black-forest-labs/flux-1.1-pro":
            if isinstance(output, list) and len(output) > 0:
                image_url = output[0]
                # Use provided local_filename or generate a unique one
                filepath = Path(local_filename) if local_filename else Path("generated_images") / f"{uuid.uuid4()}.webp"
                
                # Ensure the directory exists
                filepath.parent.mkdir(parents=True, exist_ok=True)
                
                # Download and save the image locally
                response = requests.get(image_url)
                if response.status_code == 200:
                    with open(filepath, 'wb') as file:
                        file.write(response.content)
                    
                    # Return the local file path and the URL
                    return {
                        "local_path": str(filepath),
                        "url": image_url
                    }
                else:
                    logger.warning(f"Failed to download image from URL: {image_url}")
                    return image_url
            elif isinstance(output, str):
                return output
            else:
                logger.warning(f"Unexpected output format from Replicate API for flux-1.1-pro: {output}")
                return str(output)
        else:
            if isinstance(output, list) and len(output) > 0:
                # Use provided local_filename or generate a unique one
                filepath = Path(local_filename) if local_filename else Path("generated_images") / f"{uuid.uuid4()}.webp"
                
                # Ensure the directory exists
                filepath.parent.mkdir(parents=True, exist_ok=True)
                
                # Save the image locally
                with open(filepath, 'wb') as file:
                    file.write(output[0].read())
                
                # Return the local file path and the URL
                return {
                    "local_path": str(filepath),
                    "url": output[0].url
                }
            else:
                logger.warning(f"Unexpected output format from Replicate API: {output}")
                return str(output)
    except Exception as e:
        logger.error(f"An error occurred during image generation: {str(e)}")
        return f"An error occurred during image generation: {str(e)}"
