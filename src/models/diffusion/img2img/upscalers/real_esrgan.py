import requests
from flushai.models.diffusion.img2img.img2imgbase import Img2ImgBase
from flushai.utilities.io_types import IOType
from PIL import Image
from io import BytesIO

class RealESRGAN(Img2ImgBase):
    ENDPOINT = 'https://ypaqg548s7.execute-api.us-east-2.amazonaws.com/testing/upscale'

    def __init__(self, api_key, scale):
        if scale != 2 and scale != 4 and scale != 8: 
            raise ValueError("Upscaling scale must be either 2, 4, or 8.")
        
        self.api_key = api_key
        self.input_type = IOType.IMAGE
        self.output_type = IOType.IMAGE
        self.scale = scale
        
    def generate(self, image):        
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }
    
        payload = {
            "upscale": self.scale,
            "image_urls": image,
            "mode": "url"
        }

        payload = {k: v for k, v in payload.items() if v is not None}

        if not isinstance(image, Image.Image):
            try:
                response = requests.get(image)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
                img.verify()  # Verify the integrity of the image
            except (requests.RequestException, IOError, SyntaxError) as e:
                raise ValueError(f"The image at {image} is not valid or cannot be accessed.") from e

        response = requests.post(self.ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # This line will raise an HTTPError if the HTTP request returned an unsuccessful status code
        result = response.json()
        urls = result['urls']
        final_urls = self._wait_for_images_to_be_accessible(urls=urls)
        return final_urls