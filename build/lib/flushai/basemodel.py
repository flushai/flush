from abc import ABC, abstractmethod

class BaseModel(ABC):
    """
    Abstract base class to represent a Model instance.
    """

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def generate(self, *args, **kwargs):
        pass

