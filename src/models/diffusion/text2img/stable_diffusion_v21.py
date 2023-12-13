from flushai.models.diffusion.text2img.text2imgbase import Txt2ImgBase

class StableDiffusionV21(Txt2ImgBase):
    def __init__(self, api_key):
        super().__init__(api_key, model_id="stable-diffusion-v21")