import os
import time
import json

from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from .log_ger import logging
from .utils import to_dd_mm_yyyy

logger = logging.getLogger(__name__)

class GeminiStructure:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    def get_meta_info(self, raw_image) -> str:
        start_time = time.time()

        prompt = """
            This is bank statement page. Give me a list of pointers to describe the table structure. It should among others include the following - 

            1. How is the table structured to determine a debit or a credit transaction
            2. Where is the date column and how is it structured
            3. Mention position of each column in the table
        """

        # default info
        result = """
            1. The data is in a tabular format
            2. Each transaction lies in a table row
            3. To determine if transaction is debit or credit transaction the table can be structured in either of two ways. You need to determine and choose
            between one of the two - 
                a. There are two columns - one for debit and other for credit. In most cases the left of the two is a debit column and the right is for credit
                b. One column which tells the type of the transaction. Possible types in bank statements are - DR (for debit), CR (for credit), Withdrawal, Deposit etc.
            """

        try:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[prompt, raw_image]
            )
            result = response.text
        
        except Exception as e:
            logger.error(f"Error getting meta info from page: {e}")

        end_time = time.time()
        elapsed_time = end_time - start_time

        logger.info(f"Generated meta info in {elapsed_time:.4f} seconds")

        return result

    def process(self, raw_image, meta_info: str):
        # TODO: https://ai.google.dev/gemini-api/docs/structured-output?lang=python#supply-schema-in-config

        prompt = f"""Extract transactions from this bank statement as a JSON array in the provided format.
        You can use following meta information to accurately extract the information from the table - 

        {meta_info}

        Always consider the table structure as source of truth to determine if transaction is debit or credit. Do not rely on narration in any case.

        After extraction categorize each transaction in one word in lowercase as per following rules :-

        1. Category will define the service or to the person on which the spend was made.
        2. Category information can be extracted from the description. For ex - Swiggy, Zomato, Digitalocean, Rishabh (persons name) etc.
        3. It is possible for two transactions with same category with different types - credit and debit
        

        Format:

        'type' field should be debit or credit.
        'date' must be in DD-MM-YYYY format
        'amount' should be float

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

        try:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[prompt, raw_image]
            )

            cleaned = response.text.strip('`json\n').strip('```')
            transactions = json.loads(cleaned)

            for t in transactions:
                t['date'] = to_dd_mm_yyyy(t['date'])

            return transactions
        except Exception as e:
            logger.error(f"Error processing page: {e}")
            return []
    
    def _process_serial(self, raw_images, meta_info: str):
        results = []

        total_time = 0

        for idx, raw_image in enumerate(raw_images):

            start_time = time.time()
            transactions = self.process(
                raw_image=raw_image,
                meta_info=meta_info
            )
            results.extend(
                transactions
            )
            end_time = time.time()
            elapsed_time = end_time - start_time
            total_time += elapsed_time


            logger.info(f"Processed page {idx + 1} in {elapsed_time:.4f} seconds")

            del raw_image
            del transactions

        return results
    
    def _process_parallel(self, raw_images, meta_info: str):
        start_time = time.time()

        results = []

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.process, img, meta_info) for img in raw_images]

            for future in as_completed(futures):
                result = future.result()
                results.extend(result)

        end_time = time.time()
        elapsed_time = end_time - start_time

        logger.info(f"Processed {len(raw_images)} page(s) in {elapsed_time:.4f} seconds")
        
        return results

    def process_all(self, raw_images, meta_info: str, parallel: bool = True):
        logger.info(f"Total pages to process: {len(raw_images)}")

        if parallel: 
            return self._process_parallel(
                raw_images=raw_images,
                meta_info=meta_info
            )
        
        return self._process_serial(
            raw_images=raw_images,
            meta_info=meta_info
        )
