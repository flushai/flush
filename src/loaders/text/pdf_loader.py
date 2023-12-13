import fitz
from flushai.loaders.base_loader import BaseLoader

class PDFLoader(BaseLoader):
    def __init__(self):
        pass

    def load(self, pdf_path):
        with fitz.open(pdf_path) as pdf:
            text = ""
            # Iterate over each page
            for page_num in range(len(pdf)):
                # Get the page
                page = pdf[page_num]
                # Extract text from the page
                text += page.get_text()
        return text