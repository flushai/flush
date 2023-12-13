import openai
from flushai.models.diffusion.text2img.text2imgbase import Txt2ImgBase

class DALLE(Txt2ImgBase):
    def __init__(self, api_key):
        openai.api_key = api_key

    def generate(self, prompt, num_images=4, size=512):
        urls = []
        size = str(size) + "x" + str(size)

        response = openai.Image.create(
            prompt=prompt,
            n=num_images,
            size=size
        )

        for image_data in response['data']:
            urls.append(image_data['url'])

        return urls