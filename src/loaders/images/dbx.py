import os
import dropbox
from flushai import ImageGallery
from flushai.loaders.base_loader import BaseLoader
import io

class DropboxLoader(BaseLoader):
    def __init__(self, access_token, folder_path):
        self.access_token = access_token
        self.folder_path = folder_path
        self.dbx = dropbox.Dropbox(self.access_token)

    def load(self, num_images=None):
        files = self._list_files()
        fetched_images = 0

        # Initialize an ImageGallery object
        gallery = ImageGallery()

        for file in files:
            if isinstance(file, dropbox.files.FileMetadata):
                if num_images and fetched_images >= num_images:
                    return gallery  # Return the gallery when the desired number of images is reached
                print(f"Downloading {file.name}...")
                metadata, response = self.dbx.files_download(path=file.path_lower)

                # Remove the file extension from the name
                file_name_without_extension = os.path.splitext(file.name)[0]

                # Convert the response content to bytes and add to the gallery
                img_data = io.BytesIO(response.content)
                gallery.add_image_from_bytes(img_data.getvalue(), file_name_without_extension)
                fetched_images += 1

        return gallery  # Return the gallery after downloading and adding all images

    def _list_files(self):
        try:
            return self.dbx.files_list_folder(self.folder_path).entries
        except dropbox.exceptions.ApiError as e:
            print(f"API error: {e}")
            return []
