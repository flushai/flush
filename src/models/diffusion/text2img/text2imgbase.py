import requests
from typing import Optional
import time
from flushai.models.basemodel import BaseModel
from flushai.utilities.io_types import IOType

class Txt2ImgBase(BaseModel):
    
    ENDPOINT = 'https://api.flushai.cloud/api/v1/images/txt2img'

    def __init__(self, api_key, model_id):
        self.api_key = api_key
        self.model_id = model_id
        self.input_type = IOType.TEXT
        self.output_type = IOType.IMAGE

    def generate(self, prompt: str, num_images: int = 4, steps: int = 20, seed: Optional[int] = None, negative_prompt: Optional[str] = None, height: int = None, width: int = None, prompt_strength: Optional[float] = 7.5) -> str:
        height = 1024 if self.model_id == "stable-diffusion-xl" else 520 if height == None else height
        width = 1024 if self.model_id == "stable-diffusion-xl" else 520 if width == None else width

        if prompt == "":
            raise ValueError("The prompt is empty.")
        if num_images > 4 or num_images < 1:
            raise ValueError("Number of images must be between 1 - 4.")
        if steps > 60 or steps < 10: 
            raise ValueError("Steps must be between 10 - 60")
        if height > 1024 or width > 1024 or height < 128 or width < 128:
            raise ValueError("Height and width must be between 128 - 1024")
        if (height % 8 != 0) or (width % 8 != 0):
            raise ValueError("Height and width must be multiples of 8")
        if prompt_strength > 20 or prompt_strength < 0:
            raise ValueError("Prompt strength must be between 0 and 20")

        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }
        
        payload = {
            'prompt': prompt, 
            "model_id": self.model_id, 
            'negative_prompt': negative_prompt, 
            'num_images': num_images, 
            'seed': seed, 
            'steps': steps, 
            'height': height, 
            'width': width, 
            'scale': prompt_strength
        }

        payload = {k: v for k, v in payload.items() if v is not None}
        response = requests.post(self.ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # This line will raise an HTTPError if the HTTP request returned an unsuccessful status code
        result = response.json()
        urls = result['urls']
        final_urls = self._wait_for_images_to_be_accessible(urls=urls)
        return final_urls