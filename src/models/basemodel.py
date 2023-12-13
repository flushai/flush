from abc import ABC, abstractmethod
from flushai.utilities.io_types import IOType
import time
import requests

class BaseModel(ABC):
    """
    Abstract base class to represent a Model instance.
    """
    input_type: IOType
    output_type: IOType

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def generate(self, *args, **kwargs):
        pass

    def _is_url_accessible(self, url):
        try:
            response = requests.head(url)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def _wait_for_images_to_be_accessible(self, urls):
        final_urls = []

        while urls:
            for url in urls[:]:
                if self._is_url_accessible(url):
                    urls.remove(url)
                    final_urls.append(url)

            if urls:
                time.sleep(1)

        return final_urls
