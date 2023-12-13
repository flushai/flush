from flushai.models.diffusion.text2img.text2imgbase import Txt2ImgBase
from flushai.models.diffusion.img2img.img2imgbase import Img2ImgBase
from flushai.exceptions.chain_error import ChainException
from flushai.utilities.io_types import IOType

class Chain:
    def __init__(self, **stages):
        self.stages = stages
        
    def run(self, **kwargs):
        outputs = []
        last_output = kwargs  # initialize last_output with the input arguments
        last_output_type = None
        current_output = None

        for key, stage in self.stages.items():
            model, template_or_image, *params = stage

            # Check if output type of previous model and input type of current model match.
            if last_output_type is not None and model.input_type != last_output_type and model.input_type != IOType.BOTH:
                raise ChainException(f"Output type of previous stage ('{last_output_type}') "
                                     f"is not compatible with input type of current model ('{model.input_type}')")

            if model.input_type == IOType.TEXT or (model.input_type == IOType.BOTH and 'image' in params[0] and 'prompt' not in params[0]): # The previous output is text
                formatted_prompt = template_or_image.format(**last_output)

                if (isinstance(model, Txt2ImgBase) or isinstance(model, Img2ImgBase)) and params:
                    param_dict = params[0] if params and isinstance(params[0], dict) else {}
                    current_outputs = outputs[-1] if outputs else {}
                    formatted_params = {k: v.format(**current_outputs) if isinstance(v, str) else v for k, v in param_dict.items()}
                    current_output = model.generate(prompt=formatted_prompt, **formatted_params)
                else:
                    current_output = model.generate(formatted_prompt)
            elif model.input_type == IOType.IMAGE or (model.input_type == IOType.BOTH and 'prompt' in params[0] and 'image' not in params[0]): # The previous output is an image
                prev_image = template_or_image.format(**last_output)
                param_dict = params[0] if params and isinstance(params[0], dict) else {}
                current_output = model.generate(image=prev_image, **param_dict)      
            else:
                expected_input_type = "IMAGE" if 'prompt' in params[0] else "TEXT"
                raise ValueError(f"Invalid input for the model: Expected input type is '{expected_input_type}', "
                                "or required parameters are missing in the 'params' dictionary.")


            if key:
                last_output = {key: current_output}
                outputs.append(last_output)
            
            last_output_type = model.output_type

        return current_output