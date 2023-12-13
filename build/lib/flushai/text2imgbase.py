import requests
from typing import Optional
from .basemodel import BaseModel
import time

class Txt2ImgBase(BaseModel):
    """
    Txt2ImgModel is a model to generate images based on textual prompts.
    """
    
    ENDPOINT = 'https://ypaqg548s7.execute-api.us-east-2.amazonaws.com/testing/'

    def __init__(self, api_key):
        """
        Initializes a new instance of Txt2ImgModel.
        """
        self.api_key = api_key
    def list_base_models(self):
        print("stable-diffusion-xl\nstable-diffusion-v15\nstable-diffusion-v21\npenjourney-v4\nopenjourney-v1\nanything-v5")

    def generate(self, model_id: str, prompt: str, num_images: int = 4, seed: Optional[int] = None, negative_prompt: Optional[str] = None, steps: Optional[int] = None, height: int = None, width: int = None, prompt_strength: Optional[float] = None) -> str:
        """
        Generates images based on the given textual prompt.

        Parameters:
        - prompt: The main textual prompt for image generation.
        - model_id: The model ID to use for generation.
        - ... [other parameters]
        
        Returns:
        - URLs of the generated images.
        """

        height = 1024 if model_id == "stable-diffusion-xl" else 520 if height == None else height
        width = 1024 if model_id == "stable-diffusion-xl" else 520 if width == None else width
        if prompt == "":
            raise ValueError("The prompt is empty.")
        if num_images and (num_images > 4 or num_images < 1):
            raise ValueError("Number of images must be between 1 - 4.")
        if steps and (steps > 60 or steps < 10): 
            raise ValueError("Steps must be between 10 - 60")
        if (height and height > 1024) or (width and width > 1024) or (height and height < 128) or (width and width < 128):
            raise ValueError("Height and width must be between 128 - 1024")
        if (height and height % 8 != 0) or (width and width % 8 != 0):
            raise ValueError("Height and width must be multiples of 8")
        if prompt_strength and (prompt_strength > 20 or prompt_strength < 0):
            raise ValueError("Prompt strength must be between 0 and 20")

        def is_url_accessible(url):
            try:
                response = requests.head(url)
                # 200 means OK. You might want to add more status codes as per your requirement.
                return response.status_code == 200
            except requests.RequestException:
                return False

        def wait_for_images_to_be_accessible(urls):
            final_urls = []
            while urls:
                for url in urls[:]:  # Iterating over a slice of urls to avoid issues while removing inside the loop
                    if is_url_accessible(url):
                        urls.remove(url)
                        final_urls.append(url)

                if urls:
                    time.sleep(1)
            return final_urls

        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }
        
        url = self.ENDPOINT + 'predict'
        payload = {
            'prompt': prompt, 
            "model_id": model_id, 
            'negative_prompt': negative_prompt, 
            'num_images': num_images, 
            'seed': seed, 
            'steps': steps, 
            'height': height, 
            'width': width, 
            'scale': prompt_strength
        }

        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
            result = response.json()
            urls = result['urls']
            final_urls = wait_for_images_to_be_accessible(urls)
            return final_urls
        except requests.RequestException as error:
            print('Got an error.')
