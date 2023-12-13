# pip3 install flushai

from flushai.models.diffusion.text2img import Txt2ImgBase

# Create a reference to your model on Flush
model = Txt2ImgBase(api_key = "zSYpqIgyuaAFabk7oRel6kQUSlI4G1A3rSx8tF3b", 
                    model_id = "stable-diffusion-xl")

# You must input the prompt as well as the model id. All 
# other parameters are optional. Below is a basic example:
result = model.generate(
    prompt = "a car driving on a highway, beautiful, rustic", 
    negative_prompt = 'blurry, low quality', 
    num_images = 4,
    height = 512, 
    width = 512, 
    steps = 25, 
    prompt_strength = 7.5, 
    seed = 5
)[0]