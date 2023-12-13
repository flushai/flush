from flushai.models.diffusion.img2img.img2imgbase import Img2ImgBase

class StableDiffusionV15(Img2ImgBase):
    def __init__(self, api_key):
        super().__init__(api_key, model_id="stable-diffusion-v15")