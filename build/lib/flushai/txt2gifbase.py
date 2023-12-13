import requests
from typing import Optional
from .basemodel import BaseModel
import time

class Txt2GifBase(BaseModel):
    """
    Txt2GifModel is a model to generate gifs based on textual prompts.
    """
    
    ENDPOINT = 'https://ypaqg548s7.execute-api.us-east-2.amazonaws.com/testing/'

    def __init__(self, api_key):
        """
        Initializes a new instance of Txt2ImgModel.
        """
        self.api_key = api_key

    def generate(self, motion_module: str, base_model: str, prompt: str, negative_prompt: Optional[str] = "", seed: Optional[int] = None, steps: Optional[int] = None, guidance_scale: Optional[float] = None) -> str:
        """
        Generates gifs based on the given textual prompt.

        Parameters:
        - prompt: The main textual prompt for gif generation.
        - model_id: The model ID to use for generation.
        - ... [other parameters]
        
        Returns:
        - URLs of the generated images.
        """
        base_models = ['CounterfeitV30_v30', 'FilmVelvia2', 'Pyramid%20lora_Ghibli_n3', 
                'TUSUN', 'lyriel_v16', 'majicmixRealistic_v5Preview', 
                'moonfilm_filmGrain10', 'moonfilm_reality20', 'rcnzCartoon3d_v10', 
                'realisticVisionV20_v20', 'toonyou_beta3']
        motion_modules = ['sd_v14', 'sd_v15', 'sd_v15_v2']
        if motion_module == "":
            raise ValueError("The motion module is empty")
        if base_model == "":
            raise ValueError("The base model is empty")
        if motion_module not in motion_modules:
            raise ValueError("Invalid motion module")
        if base_model not in base_models: 
            raise ValueError("Invalid base model")
        if prompt == "":
            raise ValueError("The prompt is empty.")
        if steps and (steps > 60 or steps < 10): 
            raise ValueError("Steps must be between 10 - 60")
        if guidance_scale and (guidance_scale > 20 or guidance_scale < 0):
            raise ValueError("Prompt strength must be between 0 and 20")

        def is_url_accessible(url):
            try:
                response = requests.head(url)
                # 200 means OK. You might want to add more status codes as per your requirement.
                return response.status_code == 200
            except requests.RequestException:
                return False

        def wait_for_gifs_to_be_accessible(urls):
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
        
        url = self.ENDPOINT + 'creategif'
        payload = {
            'base_model': base_model, 
            'motion_module': motion_module,
            'prompt': prompt, 
            'negative_prompt': negative_prompt, 
            'seed': seed, 
            'steps': steps, 
            'scale': guidance_scale
        }

        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
            result = response.json()
            urls = result['urls']
            final_urls = wait_for_gifs_to_be_accessible(urls)
            return final_urls
        except requests.RequestException as error:
            print('Got an error.')
