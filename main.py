import requests
from PIL import Image

from statements.extract import TextExtractor, ImageExtractor
from statements.text_structure import TextStructure
from statements.image_structure import ImageStructure


pdf_path = "/home/braveheart/Documents/statements/test/Acct Statement_XX6119_29032025.pdf"

# raw_text = TextExtractor().extract(
#     pdf_path=pdf_path
# )
# extracted_txns = TextStructure().process(
#     raw_text=raw_text
# )

# print(extracted_txns)


# raw_images = ImageExtractor().extract(
#     pdf_path=pdf_path
# )

# for raw_image in raw_images:
#     extracted_txns = ImageStructure().process(
#         raw_image=raw_image
#     )

#     print(extracted_txns)

image_url = 'https://www.ilankelman.org/stopsigns/australia.jpg'
raw_image = Image.open(requests.get(image_url, stream=True).raw)

extracted_txns = ImageStructure().process(
    raw_image=raw_image
)
print(extracted_txns)