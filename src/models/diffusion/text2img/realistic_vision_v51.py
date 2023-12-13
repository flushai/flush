from flushai.models.diffusion.text2img.text2imgbase import Txt2ImgBase

class RealisticVisionV51(Txt2ImgBase):
    def __init__(self, api_key):
        super().__init__(api_key, model_id="realistic-vision-v51")