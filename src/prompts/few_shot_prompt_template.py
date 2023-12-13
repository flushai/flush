import re
from flushai.prompts.base_prompt_template import BasePromptTemplate

class FewShotPromptTemplate(BasePromptTemplate):
    def __init__(self, examples, template, introduction=None):
        super().__init__(template)
        self.introduction = introduction  # Optional introductory line
        self.examples = examples  # List of example tuples with input and output
        self.placeholders = self._extract_placeholders(template)  # Extract placeholders

    def format(self, *args, **kwargs):
        if args:
            raise ValueError("No positional arguments are allowed. Please provide only keyword arguments.")
        
        # Check if any positional arguments are provided
        if len(kwargs) != len(self.placeholders):
            raise ValueError(f"Incorrect number of arguments provided. Expected {len(self.placeholders)} arguments, got {len(kwargs)}.")

        # Check if all placeholders have corresponding values in kwargs
        for placeholder in self.placeholders:
            if placeholder not in kwargs:
                raise ValueError(f"Missing value for placeholder '{placeholder}'.")

        # Format each example
        formatted_examples = '\n'.join([self._format_example(ex) for ex in self.examples])

        # Format the main template with keyword arguments
        formatted_main = self.template.format(**kwargs)
        
        # Combine introduction, examples, and main template
        full_prompt = ((self.introduction or '') + '\n\n' + formatted_examples + '\n' + formatted_main).strip()
        return full_prompt

    def _format_example(self, example):
        input_part, output_part = example
        return f"{input_part}\n{output_part}\n"  # Restored 'Input:' and 'Output:' if needed
