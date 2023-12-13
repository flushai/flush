import os
from PIL import Image
from flushai import ImageGallery
from flushai.loaders.base_loader import BaseLoader
from io import BytesIO

class DirectoryLoader(BaseLoader):
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def load(self, num_images=None):
        files = self._list_files()
        fetched_images = 0

        # Initialize an ImageGallery object
        gallery = ImageGallery()

        for file_name in files:
            if num_images and fetched_images >= num_images:
                break  # Stop if the desired number of images is reached

            file_path = os.path.join(self.folder_path, file_name)
            if os.path.isfile(file_path):
                try:
                    print(f"Loading {file_name}...")
                    with Image.open(file_path) as img:
                        # Convert the image to bytes
                        img_byte_arr = BytesIO()
                        img.save(img_byte_arr, format=img.format)
                        gallery.add_image_from_bytes(img_byte_arr.getvalue(), file_name)
                        fetched_images += 1
                except IOError:
                    print(f"Cannot load {file_name}. Unsupported image format or corrupted file.")
        
        return gallery  # Return the gallery after adding all images

    def _list_files(self):
        # List all files in the directory that are not subdirectories
        return [f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))]
