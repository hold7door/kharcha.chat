from statements.extract import TextExtractor
from statements.structure import Structure


pdf_path = "/opt/statements/test/Acct Statement_XX6119_29032025.pdf"


raw_text = TextExtractor().extract(
    pdf_path=pdf_path
)
extracted_txns = Structure().process(
    raw_text=raw_text
)

print(extracted_txns)