from typing import List
from flushai import ImageGallery
from flushai.loaders.base_loader import BaseLoader, download_webp_image
from pexels_api import API

class PexelsAPIWrapper(BaseLoader):
    """
    PexelsAPIWrapper is a class that interacts with the Pexels API.
    It retrieves image links based on the provided search query and returns an ImageGallery object containing those images.
    """

    def __init__(self, api_key: str):
        """
        Initializes the PexelsAPIWrapper with the provided API key.

        Parameters:
            api_key (str): The API key for accessing the Pexels API.
        """
        self.api_key = api_key

    def load(self, query: str, num: int = 10) -> ImageGallery:
        """
        Searches the Pexels API for images based on the provided query.

        Parameters:
            query (str): The search query.
            num (int): The number of images to fetch. Default is 10.

        Returns:
            ImageGallery: An ImageGallery object containing the downloaded images.
        """
        api = API(self.api_key)
        
        # Calculate how many iterations are needed to fetch 'num' images
        # Pexels API has a maximum limit of 80 results per page
        iterations = num // 80 + (1 if num % 80 != 0 else 0)

        # Initialize an ImageGallery object.
        gallery = ImageGallery()

        image_count = 0
        break_outer_loop = False

        for i in range(1, iterations + 1):
            api.search(query, results_per_page=80, page=i)
            images = api.get_entries()

            for image in images:
                downloaded_image_data = download_webp_image(image.original)

                if downloaded_image_data:
                    gallery.add_image_from_bytes(downloaded_image_data, f"image_{image_count}.webp")
                    image_count += 1

                if image_count == num:
                    break_outer_loop = True
                    break

            if break_outer_loop:
                break

        return gallery
    