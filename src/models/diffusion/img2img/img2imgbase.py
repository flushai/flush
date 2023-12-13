import requests
from flushai.models.basemodel import BaseModel
from flushai.utilities.io_types import IOType
from PIL import Image
from io import BytesIO
import base64

class Img2ImgBase(BaseModel):
    ENDPOINT = 'https://api.flushai.cloud/api/v1/images/img2img'

    def __init__(self, api_key, model_id):
        self.api_key = api_key
        self.model_id = model_id
        self.input_type = IOType.BOTH
        self.output_type = IOType.IMAGE

    def generate(self, prompt, image, negative_prompt = None, seed = None, num_images = 2, steps = 20, prompt_strength = 7.5, noise = 0.75):
        if not prompt or prompt == "":
            raise ValueError("The prompt is empty.")
        if steps > 60 or steps < 10: 
            raise ValueError("Steps must be between 10 - 60")
        if num_images < 1 or num_images > 4:
            raise ValueError("Number of images must be between 1 - 4")
        if prompt_strength > 20 or prompt_strength < 0:
            raise ValueError("Prompt strength must be between 0 and 20")
                
        if not isinstance(image, Image.Image):
            try:
                response = requests.get(image)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
                img.verify()  # Verify the integrity of the image
            except (requests.RequestException, IOError, SyntaxError) as e:
                raise ValueError(f"The image at {image} is not valid or cannot be accessed.") from e
        else:
            buffer = BytesIO()
            image.save(buffer, format="JPEG")
            image_bytes = buffer.getvalue()
            image_base64 = base64.b64encode(image_bytes)
            image = image_base64.decode('utf-8')

        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }
    
        payload = {
            "model_id": self.model_id,
            "prompt": prompt, 
            "negative_prompt": negative_prompt,
            "input_image": image, 
            "seed": seed,
            "num_images": num_images,
            "num_steps": steps,
            "scale": prompt_strength, 
            "noise": noise
        }

        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(self.ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # This line will raise an HTTPError if the HTTP request returned an unsuccessful status code
        result = response.json()
        urls = result['urls']
        final_urls = self._wait_for_images_to_be_accessible(urls=urls)
        return final_urls