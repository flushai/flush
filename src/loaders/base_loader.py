from abc import ABC, abstractmethod
import requests

class BaseLoader(ABC):
    """
    Abstract class to represent a generic cloud storage loader.
    """

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def load(self, *args, **kwargs):
        """
        Downloads a specified number of images and returns an image gallery object.
        """
        pass

def download_webp_image(url):
    """
    Helper function to download an image from a given URL and return its byte data.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content  # Return image data in bytes format
    except requests.exceptions.RequestException as e:
        print("Error occurred while downloading the image:", e)
    return None