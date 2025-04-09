from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from statements.gemini_image_structure import GeminiStructure
from statements.extract import ImageExtractor

from statements.log_ger import logging

logger = logging.getLogger(__name__)

app = FastAPI()

gemini = GeminiStructure()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        raw_images = ImageExtractor().extract(
            pdf_path=file.file
        )

        results = gemini.process_all(raw_images, parallel=False)

        logger.info(f"Found {len(results)} transactions")

        return JSONResponse(content=results)

    except Exception as e:
        logger.exception("Error processing uploaded PDF")
        raise HTTPException(status_code=500, detail=str(e))
