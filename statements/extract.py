import pdfplumber

import warnings

warnings.filterwarnings("ignore", message="CropBox missing from /Page, defaulting to MediaBox")

class TextExtractor:
    def __init__(self) -> None:
        pass

    def extract(self, pdf_path: str) -> str:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages[:1]:
                text += page.extract_text() + "\n"
        return text.strip()

class ImageExtractor:
    def __init__(self) -> None:
        pass

    def extract(self, pdf_path: str, num_page: int = 1) -> str:
        images = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages[:min(num_page, len(pdf.pages))]:
                img = page.to_image(resolution=300).original
                images.append(img)
        return images  # List of PIL images