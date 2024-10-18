import replicate
import uuid
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

async def generate_image(prompt, model="black-forest-labs/flux-dev"):
    logger.debug(f"Generating image with prompt: {prompt}, model: {model}")
    try:
        output = await replicate.async_run(
            model,
            input={"prompt": prompt}
        )
        logger.debug(f"Raw output for {model}: {output}")
        
        if model == "black-forest-labs/flux-1.1-pro":
            if isinstance(output, list) and len(output) > 0:
                return output[0]
            elif isinstance(output, str):
                return output
            else:
                logger.warning(f"Unexpected output format from Replicate API for flux-1.1-pro: {output}")
                return str(output)
        else:
            if isinstance(output, list) and len(output) > 0:
                # Generate a unique filename
                filename = f"{uuid.uuid4()}.webp"
                filepath = Path("generated_images") / filename
                
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
