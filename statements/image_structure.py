from transformers import AutoProcessor, GenerationConfig, AutoModelForCausalLM
import torch

# Load model & processor
model_id = "microsoft/Phi-4-multimodal-instruct"

class ImageStructure:
    def __init__(self) -> None:
        self.processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
        self.generation_config = GenerationConfig.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
    
    def process(self, raw_image):
        # Prompt for transaction extraction
        prompt = f"""Extract all transactions from this bank statement image and return them in JSON format. 
        
        Sample Format:

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

        # Encode input
        inputs = self.processor(prompt, raw_image, return_tensors="pt")

        # Generate response
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_length=1024, generation_config=self.generation_config)

        # Decode response
        extracted_data = self.processor.decode(outputs[0], skip_special_tokens=True)

        return extracted_data

