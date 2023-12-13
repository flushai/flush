from abc import ABC, abstractmethod
import re

class BasePromptTemplate(ABC):
    def __init__(self, template):
        self.template = template
        self.placeholders = self._extract_placeholders(template)

    def _extract_placeholders(self, template):
        return re.findall(r'\{([^}]*)\}', template)
    
    def _from_template(cls, template):
        input_variables = re.findall(r'\{([^}]*)\}', template)
        return cls(input_variables, template)

    @abstractmethod
    def format(self, *args, **kwargs):
        pass

    