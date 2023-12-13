from typing import List
from serpapi import GoogleSearch
from flushai import ImageGallery
from flushai.loaders.base_loader import BaseLoader, download_webp_image

class SerpAPIWrapper(BaseLoader):
    """
    SerpAPIWrapper is a class for interacting with the SerpAPI using the Google Images engine.
    It retrieves image links based on a search query and returns an ImageGallery object containing those images.
    """

    def __init__(self, api_key: str):
        """
        Initializes the SerpAPIWrapper with the provided API key.

        Parameters:
            api_key (str): The API key for accessing SerpAPI.
        """
        self._api_key = api_key  # Made the variable private as it shouldn't be accessed directly

    def load(self, query: str, num: int = 10) -> ImageGallery:
        """
        Searches the Google Images engine through SerpAPI based on the provided query.

        Parameters:
            query (str): The search query.
            num (int): The number of images to retrieve. Default is 10.

        Returns:
            ImageGallery: An ImageGallery object containing the downloaded images.
        """
        # Calculate the number of iterations needed, considering the limit of 100 results per page
        iterations = num // 100 + (1 if num % 100 != 0 else 0)

        # Initialize an ImageGallery object.
        gallery = ImageGallery()

        image_count = 0
        break_outer_loop = False  # Flag to break the outer loop when the desired number of images is reached

        for i in range(iterations):
            params = {
                "q": query,
                "engine": "google_images",
                "api_key": self._api_key,
                "ijn": i
            }

            try:
                results = GoogleSearch(params).get_dict()
            except Exception as e:
                print(f"An error occurred while querying the API: {e}")
                return gallery  # Return the images downloaded so far

            # Check if an error occurred during the search
            if "error" in results:
                print(f"An error occurred: {results['error']}")
                continue

            images_results = results["images_results"]

            for image in images_results:
                downloaded_image_data = download_webp_image(image["original"])

                if downloaded_image_data:
                    gallery.add_image_from_bytes(downloaded_image_data, f"image_{image_count}.webp")
                    image_count += 1

                if image_count == num:
                    break_outer_loop = True
                    break

            if break_outer_loop:
                break

        return gallery
