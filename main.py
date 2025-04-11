import json
import math
import time
import requests

from PIL import Image

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from statements.log_ger import logging

logger = logging.getLogger(__name__)

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
    num_page=1
)

all_txns = []


gemini = GeminiStructure()

# extract table information

meta_info = gemini.get_meta_info(
    raw_image=raw_images[0]
)

# single
# for raw_image in raw_images:
#     start_time = time.time()

#     extracted_txns = gemini.process(
#         raw_image=raw_image
#     )
    
#     end_time = time.time()
#     elapsed_time = end_time - start_time

#     logger.info(f"Processed page in {elapsed_time:.2f} seconds")

#     all_txns.extend(extracted_txns)

# multiple


all_txns = gemini.process_all(
    raw_images=raw_images,
    meta_info=meta_info,
    parallel=False
)

for idx, txn in enumerate(all_txns):
    txn["id"] = f"txn{idx+1}"

# Write to file with indentation
with open("output.json", "w") as f:
    json.dump(all_txns, f, indent=4)
