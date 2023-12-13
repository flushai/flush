import re
from flushai.prompts.base_prompt_template import BasePromptTemplate

class PromptTemplate(BasePromptTemplate):
    def __init__(self, template):
        super().__init__(template)
        self.input_variables = self._extract_placeholders(template)
        self.placeholders = self.input_variables  # Assuming placeholders are the same as input variables

    def format(self, *args, **kwargs):
        if args:
            raise ValueError("No positional arguments are allowed. Please provide only keyword arguments.")
    
        if len(kwargs) != len(self.placeholders):
            raise ValueError(f"Incorrect number of arguments provided. Expected {len(self.placeholders)}, got {len(kwargs)}.")

        for placeholder in self.placeholders:
            if placeholder not in kwargs:
                raise ValueError(f"Missing value for placeholder '{placeholder}'.")

        formatted_template = self.template
        for placeholder, value in kwargs.items():
            formatted_template = formatted_template.replace("{" + placeholder + "}", str(value))

        return formatted_template


    
