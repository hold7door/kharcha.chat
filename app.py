from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import io
import os
import json
import math
from PIL import Image

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse

from kharcha.gemini_image_structure import GeminiStructure
from kharcha.extract import ImageExtractor
from kharcha.log_ger import logging

logger = logging.getLogger(__name__)



app = FastAPI()

# Allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ALLOW_ORIGIN")],  # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gemini = GeminiStructure()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        # Read the uploaded PDF file
        pdf_bytes = await file.read()

        # Extract images from the PDF
        raw_images = ImageExtractor().extract(
            pdf_path=pdf_bytes,
            num_page=math.inf
        )

        if not raw_images:
            raise HTTPException(status_code=400, detail="No images extracted from PDF.")

        # Extract table structure information from the first page
        meta_info = gemini.get_meta_info(raw_image=raw_images[0])

        # Define a generator to process each image and yield transactions
        def transaction_generator():
            for idx, raw_image in enumerate(raw_images):
                transactions = gemini.process(raw_image, meta_info)
                for txn in transactions:
                    txn["id"] = f"txn{idx+1}"
                    yield txn
                # Explicitly delete variables to free memory
                del raw_image
                del transactions

        # Create a streaming response to yield transactions as JSON
        return StreamingResponse(
            (json.dumps(txn) + "\n" for txn in transaction_generator()),
            media_type="application/json"
        )

    except Exception as e:
        logger.exception("Error processing uploaded PDF")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-image/")
async def upload_images(file: UploadFile = File(...)):
    # Check that all uploaded files are PNGs

    if not file.filename.endswith(".png"):
        raise HTTPException(status_code=400, detail="Only PNG files are supported.")

    try:
        # Read all uploaded images
        raw_image = await file.read()

        raw_image = Image.open(io.BytesIO(raw_image))

        results = []

        # extract table information

        meta_info = """
        1. The data is in a tabular format
        2. Each transaction lies in a table row
        3. To determine if transaction is debit or credit transaction the table can be structured in either of two ways. You need to determine and choose
        between one of the two - 
            a. There are two columns - one for debit and other for credit. In most cases the left of the two is a debit column and the right is for credit
            b. One column which tells the type of the transaction. Possible types in bank statements are - DR (for debit), CR (for credit), Withdrawal, Deposit etc.
        """

        results = gemini.process_all([raw_image], meta_info=meta_info, parallel=False)
        
        logger.info(f"Found {len(results)} transactions")

        return JSONResponse(content=results)

    except Exception as e:
        logger.exception("Error processing uploaded images")
        raise HTTPException(status_code=500, detail=str(e))