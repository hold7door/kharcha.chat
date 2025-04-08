import os
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from .log_ger import logging

logger = logging.getLogger(__name__)

class GeminiStructure:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def process(self, raw_image):
        prompt = """Extract transactions from this bank statement as a JSON array in the provided format.

        After extraction categorize each transaction in one word.
        Category will define the service on which the spend was made.
        Category information can be extracted from the description. For ex - Swiggy, Zomato, Digitalocean etc.

        'type' field should be debit or credit

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

    def process_all(self, raw_images):
        results = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.process, img) for img in raw_images]

            for future in as_completed(futures):
                result = future.result()
                results.extend(result)

        return results
