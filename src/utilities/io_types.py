from enum import Enum, auto

class IOType(Enum):
    TEXT = auto()
    IMAGE = auto()
    BOTH = auto()

    def __str__(self):
        return self.name.lower()