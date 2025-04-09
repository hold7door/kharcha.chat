import os
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from .log_ger import logging

logger = logging.getLogger(__name__)

class GeminiStructure:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def process(self, raw_image):
        # TODO: https://ai.google.dev/gemini-api/docs/structured-output?lang=python#supply-schema-in-config

        prompt = """Extract transactions from this bank statement as a JSON array in the provided format.

        After extraction categorize each transaction in one word in lowercase.
        Category will define the service on which the spend was made.
        Category information can be extracted from the description. For ex - Swiggy, Zomato, Digitalocean etc.

        'type' field should be debit or credit.
        'date' must be in DD-MM-YYYY format

        Format:

        [
            {
                "date": "YYYY-MM-DD",
                "description": "Transaction details",
                "amount": 123.45,
                "type": "debit/credit",
                "category": "Swiggy"
            }
        ]

        Return ONLY JSON. Do not include explanations.
        """

        try:
            response = self.client.models.generate_content(
                model='gemini-1.5-flash',
                contents=[prompt, raw_image]
            )

            cleaned = response.text.strip('`json\n').strip('```')
            transactions = json.loads(cleaned)

            return transactions
        except Exception as e:
            logger.error(f"Error processing page: {e}")
            return []
    
    def _process_serial(self, raw_images):
        results = []

        total_time = 0

        for idx, raw_image in enumerate(raw_images):
            start_time = time.time()
            results.extend(
                self.process(
                    raw_image=raw_image
                )
            )
            end_time = time.time()
            elapsed_time = end_time - start_time
            total_time += elapsed_time

            logger.info(f"Processed {idx+1} page(s) in {total_time:.4f} seconds")
        
        return results
    
    def _process_parallel(self, raw_images):
        start_time = time.time()

        results = []

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.process, img) for img in raw_images]

            for future in as_completed(futures):
                result = future.result()
                results.extend(result)

        end_time = time.time()
        elapsed_time = end_time - start_time

        logger.info(f"Processed {len(raw_images)} page(s) in {elapsed_time:.4f} seconds")
        
        return results

    def process_all(self, raw_images, parallel: bool = True):
        logger.info(f"Total pages to process: {len(raw_images)}")

        if parallel: 
            return self._process_parallel(
                raw_images=raw_images
            )
        
        return self._process_serial(
            raw_images=raw_images
        )
