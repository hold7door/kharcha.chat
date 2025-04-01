import re
import json
import torch
from .log_ger import logging
from typing import Tuple

from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

logger = logging.getLogger(__name__)

MODEL_NAME = "deepseek-ai/deepseek-coder-1.3b-instruct"


class TextStructure:
    def __init__(self):
        self.tokenizer, self.model = self.load_model()
    
    def load_model(self) -> Tuple[AutoTokenizer, AutoModelForCausalLM]:
        model_name = MODEL_NAME
        logger.info(f"Loading model: {model_name}")

        # Load model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Define the quantization configuration for 8-bit
        quantization_config = BitsAndBytesConfig(
            load_in_8bit=True,
            llm_int8_threshold=6.0,
        )

        # Load model
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",  #! Dynamically balancing between CPU and GPU
            quantization_config=quantization_config,  #! Quantization
        )

        logger.info(f"Model ({model_name}) loaded.")
        return tokenizer, model

    def process(self, raw_text: str) -> dict:
        # Define prompt
        prompt = f"""Extract transactions from this bank statement as a JSON array in the provided format.
        
        Bank Statement:
        {raw_text}

        Format:

        ```json
        [
        {{
            "date": "YYYY-MM-DD",
            "description": "Transaction details",
            "amount": 123.45,
            "type": "debit/credit"
        }}
        ]
        ```


        Return ONLY JSON. Do not include explanations.
        """

        # Tokenize input
        inputs = self.tokenizer(prompt, return_tensors="pt")

        # Move input tensors to the same device as the model
        device = next(self.model.parameters()).device
        
        logger.info(f"Using device: {device}")

        inputs = {key: value.to(device) for key, value in inputs.items()}

        # Generate response
        with torch.no_grad():
            output = self.model.generate(
                **inputs, 
                max_new_tokens=1024, 
                temperature=0.7,
                do_sample=True,
                top_k=50,
                top_p=0.9
            )

        # Decode output
        structured_output = self.tokenizer.decode(output[0], skip_special_tokens=True)
        logger.info(f"{structured_output=}")

        json_str = re.search(r'```json(.*?)```', structured_output, re.DOTALL).group(1)

        logger.info(f"{json_str=}")

        # Extract JSON
        try:
            transactions = json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            transactions = []

        return transactions