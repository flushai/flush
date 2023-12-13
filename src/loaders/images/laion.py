import requests
import csv
from typing import List, Optional
from flushai import ImageGallery
from flushai.loaders.base_loader import BaseLoader, download_webp_image

class LAIONWrapper(BaseLoader):
    """
    LAIONWrapper is a class to interact with the LAION Aesthetic API.
    It retrieves image links based on the search query and returns an ImageGallery object containing those images.
    """
    ENDPOINT = "https://laion-aesthetic.datasette.io/laion-aesthetic-6pls/images.csv?_labels=on&_stream=on&_search="
    
    def __init__(self):
        """
        Initializes the LAIONWrapper object.
        """
        pass
    
    def load(self, query: str, num: int = 10) -> ImageGallery:
        """
        Searches the LAION Aesthetic API for images based on the given query.

        Parameters:
            query (str): The search query.
            num (int): The number of images to return. Default is 10.

        Returns:
            ImageGallery: An ImageGallery object containing the downloaded images.
        """
        
        queried_endpoint = f"{self.ENDPOINT}{query}"
        
        try:
            response = requests.get(queried_endpoint)
            response.raise_for_status()
            csv_content = response.text
        except requests.RequestException as e:
            print(f"An error occurred while querying the API: {e}")
            return ImageGallery()  # Return an empty gallery
        
        image_count = 0

        # Initialize an ImageGallery object.
        gallery = ImageGallery()

        # Initialize a CSV reader and skip the header row.
        csv_reader = csv.reader(csv_content.splitlines())
        next(csv_reader, None)

        # Extract image links from the CSV and add them to the gallery.
        for row in csv_reader:
            downloaded_image_data = download_webp_image(row[1])

            if downloaded_image_data:
                gallery.add_image_from_bytes(downloaded_image_data, f"image_{image_count}.webp")
                image_count += 1
            
            if image_count == num:
                break
                
        return gallery
    
