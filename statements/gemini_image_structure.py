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
                
            Bank Statement:

            Format:

            [
            {{
                "date": "YYYY-MM-DD",
                "description": "Transaction details",
                "amount": 123.45,
                "type": "debit/credit"
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