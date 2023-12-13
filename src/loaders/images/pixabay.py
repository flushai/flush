from typing import List
import requests
from flushai import ImageGallery
from flushai.loaders.base_loader import BaseLoader, download_webp_image

class PixabayAPIWrapper(BaseLoader):
    """
    PixabayAPIWrapper is a class for interacting with the Pixabay API.
    It retrieves image links based on the search query and returns an ImageGallery object containing those images.
    """
    ENDPOINT = "https://pixabay.com/api/"

    def __init__(self, api_key: str):
        """
        Initializes the PixabayAPIWrapper with the provided API key.

        Parameters:
            api_key (str): The API key for accessing the Pixabay API.
        """
        self._api_key = api_key  # Made the variable private as it shouldn't be accessed directly

    def load(self, query: str, num: int = 10) -> ImageGallery:
        """
        Searches the Pixabay API for images based on the given query.

        Parameters:
            query (str): The search query.
            num (int): The number of images to retrieve. Default is 10.

        Returns:
            ImageGallery: An ImageGallery object containing the downloaded images.
        """
        # Calculate the number of iterations needed, considering the API's limit of 100 results per page
        iterations = num // 200 + (1 if num % 200 != 0 else 0)

        # Initialize an ImageGallery object.
        gallery = ImageGallery()

        image_count = 0
        break_outer_loop = False  # Flag to break the outer loop when the desired number of images is reached

        for i in range(1, iterations + 1):
            params = {
                "key": self._api_key,
                "q": query,
                "per_page": 200,
                "page": i
            }

            try:
                response = requests.get(self.ENDPOINT, params=params)
                response.raise_for_status()
                images = response.json()['hits']
            except requests.RequestException as e:
                print(f"An error occurred while querying the API: {e}")
                return gallery  # Return the images downloaded so far

            for image in images:
                downloaded_image_data = download_webp_image(image['webformatURL'])

                if downloaded_image_data:
                    gallery.add_image_from_bytes(downloaded_image_data, f"image_{image_count}.webp")
                    image_count += 1

                if image_count == num:
                    break_outer_loop = True
                    break

            if break_outer_loop:
                break

        return gallery
