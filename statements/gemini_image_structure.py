import os
import json

from google import genai

from .log_ger import logging
logger = logging.getLogger(__name__)

class GeminiStructure:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    def process(self, raw_image):
        prompt = f"""Extract transactions from this bank statement as a JSON array in the provided format.
        
            After extraction categorize each transaction in one word.
            Category will define the service on which the spend was made.
            Category information can be extracted from the description.
            For ex - Swiggy, Zomato, Digitalocean etc.

            Format:

            [
            {{
                "date": "YYYY-MM-DD",
                "description": "Transaction details",
                "amount": 123.45,
                "type": "debit/credit",
                "category": "Swiggy"
            }}
            ]


            Return ONLY JSON. Do not include explanations.
        """

        response = self.client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[
                prompt,
                raw_image
            ]
        )

        # Remove the markdown formatting
        cleaned = response.text.strip('`json\n').strip('```')

        # Parse to Python list
        transactions = json.loads(cleaned)

        return transactions