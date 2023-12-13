from PIL import Image, ImageDraw, ImageFont
import os
import io
from pillow_heif import register_heif_opener

class ImageGallery():
    def __init__(self):
        self.images = {}
        self._index = 0
        register_heif_opener()

    def __iter__(self):
        self._index = 0  # Reset the index each time someone creates an iterator
        return self
    
    def __next__(self):
        if self._index < len(self.images):
            keys = list(self.images.keys())  # Extracting the keys to a list
            key = keys[self._index]
            self._index += 1
            return key, self.images[key]
        raise StopIteration
    
    def get_image(self, image_name):
        """Return the image object corresponding to image_name."""
        if image_name in self.images:
            return self.images[image_name]
        else:
            raise KeyError(f"No image found with key {image_name}.")

    def add_image(self, image_path, image_name = None):
        if image_name is None:
            image_name = os.path.splitext(os.path.basename(image_path))[0]

        if image_name != None and image_name in self.images:
            raise ValueError(f"An image with key {image_name} already exists.")
        
        image = Image.open(image_path)
        self.images[image_name] = image
    
    def add_image_from_bytes(self, image_bytes, image_name):
        if image_name != None and image_name in self.images:
            raise ValueError(f"An image with key {image_name} already exists.")
        
        image = Image.open(io.BytesIO(image_bytes))
        self.images[image_name] = image

    def add_image_from_array(self, image_data, image_name):
        if image_name in self.images:
            raise ValueError(f"An image with key {image_name} already exists.")

        # Convert the numpy array to a PIL image
        image = Image.fromarray(image_data)

        # Add the image to the gallery
        self.images[image_name] = image

    def remove_image(self, image_name):
        if image_name not in self.images:
            raise KeyError(f"No image found with key {image_name}.")
        
        del self.images[image_name]

    def display_image(self, image_name):
        if image_name not in self.images:
            raise KeyError(f"No image found with key {image_name}.")
        
        self.images[image_name].show()

    def rotate(self, image_name, angle):
        """Rotate an image by a specified angle."""
        if image_name not in self.images:
            raise KeyError(f"No image found with key {image_name}.")
        self.images[image_name] = self.images[image_name].rotate(angle)

    def size(self):
        return len(self.images)

    def rename_image(self, old_name, new_name):
        if old_name not in self.images:
            raise KeyError(f"No image found with key {old_name}.")

        if new_name in self.images:
            raise ValueError(f"An image with key {new_name} already exists.")

        self.images[new_name] = self.images.pop(old_name)

    def display_all(self):
        if not self.images:
            print("No images to display.")
            return

        cell_size = 200  # Size of the square cell
        images_per_row = 4
        gap_size = 10
        font_size = 20
        font = ImageFont.truetype("flushai/utilities/fonts/Arial.ttf", font_size)  # Use a suitable path to your font
        text_height = font_size + 10  # Additional space for text below the images

        # Create a blank canvas for the grid
        collage_width = (cell_size + gap_size) * images_per_row - gap_size
        # Elongate each cell to accommodate the text
        collage_height = (cell_size + text_height + gap_size) * (-(-len(self.images) // images_per_row)) - gap_size
        collage = Image.new('RGB', (collage_width, collage_height), color='white')

        x_offset = 0
        y_offset = 0
        for image_name, image in self.images.items():
            # Resize images to fit within square cells
            aspect_ratio = image.width / image.height
            if aspect_ratio > 1:  # Wide image
                new_size = (cell_size, int(cell_size / aspect_ratio))
            else:  # Tall image
                new_size = (int(cell_size * aspect_ratio), cell_size)
            resized_image = image.resize(new_size, Image.ANTIALIAS)

            # Center the image within the square portion of the cell (excluding text area)
            x_centered = x_offset + (cell_size - new_size[0]) // 2
            y_centered = y_offset + (cell_size - new_size[1]) // 2

            # Paste the resized image onto the collage canvas
            collage.paste(resized_image, (x_centered, y_centered))

            # Draw the image name below the image in the reserved text area
            draw = ImageDraw.Draw(collage)
            text_width, _ = draw.textsize(image_name, font=font)
            text_x = x_offset + (cell_size - text_width) // 2
            text_y = y_offset + cell_size + (text_height - font_size) // 2  # Center text vertically in text area
            draw.text((text_x, text_y), image_name, font=font, fill="black")

            # Move to the next cell in the grid
            if ((x_offset + cell_size + gap_size) // (cell_size + gap_size)) % images_per_row == 0:
                x_offset = 0
                y_offset += cell_size + text_height + gap_size
            else:
                x_offset += cell_size + gap_size

        # Display the final collage
        collage.show()
