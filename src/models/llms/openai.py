import openai
from flushai.models.basemodel import BaseModel
from flushai.utilities.io_types import IOType

class OpenAI(BaseModel):
    input_type = IOType.TEXT
    output_type = IOType.TEXT

    def __init__(self, model_name, api_key, api_org=None, max_tokens=100, temperature=1, context=""):
        if not hasattr(self, 'input_type') or not hasattr(self, 'output_type'):
            raise NotImplementedError("Concrete implementations of BaseModel must set 'input_type' and 'output_type'.")
        
        self.model_name = model_name
        openai.api_key = api_key

        if api_org != None:
            openai.organization = api_org

        self.max_tokens = max_tokens
        self.temperature = temperature
        self.context = context

    def generate(self, prompt):
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.context},
                {"role": "user", "content": prompt},
            ],
            # max_tokens=self.max_tokens,
            temperature=self.temperature,
        )

        return response['choices'][0]['message']['content']