import json
import requests

from PIL import Image

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from statements.extract import ImageExtractor
from statements.gemini_image_structure import GeminiStructure

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

# image_url = 'https://www.ilankelman.org/stopsigns/australia.jpg'
# raw_image = Image.open(requests.get(image_url, stream=True).raw)

# extracted_txns = ImageStructure().process(
#     raw_image=raw_image
# )
# print(extracted_txns)


raw_images = ImageExtractor().extract(
    pdf_path=pdf_path,
    num_page=5
)

all_txns = []

for raw_image in raw_images:
    extracted_txns = GeminiStructure().process(
        raw_image=raw_image
    )
    all_txns.extend(extracted_txns)

for idx, txn in enumerate(all_txns):
    txn["id"] = f"txn{idx+1}"

# Write to file with indentation
with open("output.json", "w") as f:
    json.dump(all_txns, f, indent=4)