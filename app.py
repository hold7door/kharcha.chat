from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import os
import json
import math

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from statements.gemini_image_structure import GeminiStructure
from statements.extract import ImageExtractor

from statements.log_ger import logging

from statements.utils import to_dd_mm_yyyy

logger = logging.getLogger(__name__)

app = FastAPI()

gemini = GeminiStructure()

app = FastAPI()

# Allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ALLOW_ORIGIN")],  # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        # STUB TO TEST
        # with open("output.json", "r") as f:
        #     results = json.load(f)
        #     for idx, txn in enumerate(results):
        #         txn["id"] = f"txn{idx+1}"
        #         txn["date"] = to_dd_mm_yyyy(txn["date"])

        #     return JSONResponse(content=results)
        
        raw_images = ImageExtractor().extract(
            pdf_path=file.file,
            num_page=math.inf
        )
        results = []

        if raw_images:

            # extract table information

            meta_info = gemini.get_meta_info(
                raw_image=raw_images[0]
            )

            results = gemini.process_all(raw_images, meta_info=meta_info, parallel=False)

            # add a unique identifier to each image
            for idx, txn in enumerate(results):
                txn["id"] = f"txn{idx+1}"

        logger.info(f"Found {len(results)} transactions")

        # FOR TESTING ONLY
        
        # Write to file with indentation
        # with open("output.json", "w") as f:
        #     json.dump(results, f, indent=4)

        return JSONResponse(content=results)

    except Exception as e:
        logger.exception("Error processing uploaded PDF")
        raise HTTPException(status_code=500, detail=str(e))
