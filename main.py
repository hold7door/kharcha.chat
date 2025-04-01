import os
os.environ['HF_HOME'] = "/opt/transformers_cache"

from statements.extract import TextExtractor, ImageExtractor
from statements.text_structure import TextStructure
from statements.image_structure import ImageStructure


pdf_path = "/opt/statements/test/Acct Statement_XX6119_29032025.pdf"

# raw_text = TextExtractor().extract(
#     pdf_path=pdf_path
# )
# extracted_txns = TextStructure().process(
#     raw_text=raw_text
# )

# print(extracted_txns)


raw_images = ImageExtractor().extract(
    pdf_path=pdf_path
)

for raw_image in raw_images:
    extracted_txns = ImageStructure().process(
        raw_text=raw_image
    )

    print(extracted_txns)