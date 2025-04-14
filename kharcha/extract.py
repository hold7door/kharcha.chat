import time

import io
import fitz 
import pdfplumber

from PIL import Image

from .log_ger import logging
logger = logging.getLogger(__name__)


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

    def extract(self, pdf_path: str | bytes, num_page: int = 1) -> str:
        start_time = time.time()

        images = []

        # ! pdfplumber has memory leak
        # https://github.com/jsvine/pdfplumber/issues/193

        # with pdfplumber.open(pdf_path) as pdf:
        #     num_of_pages = min(num_page, len(pdf.pages))

        # for page_number in range(num_of_pages):
        #     with pdfplumber.open(pdf_path) as pdf:
        #         page = pdf.pages[page_number]
        #         img = page.to_image(resolution=600).original
        #         images.append(img)
                
        #         page.flush_cache()
        #         page.get_textmap.cache_clear()



        kwparam = {
            "filename" if type(pdf_path) == 'str' else "stream": pdf_path
        }
        logger.info(f"File type: {type(pdf_path)}")
        
        with fitz.open(**kwparam, filetype="pdf") as doc:
            num_of_pages = min(num_page, len(doc))
            logger.info(f"PDF opened. Nuber of pages: {num_of_pages}")

            for page_number in range(num_of_pages):
                page = doc.load_page(page_number)  # or doc[page_number]
                pix = page.get_pixmap(dpi=600)
                img_bytes = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_bytes))
                images.append(img)

        end_time = time.time()
        elapsed_time = end_time - start_time

        logger.info(f"Time taken to convert PDF to list of images: {elapsed_time:.4f} seconds")

        return images  # List of PIL images