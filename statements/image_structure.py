import os
import torch

from .log_ger import logging
from transformers import AutoProcessor, GenerationConfig, AutoModelForCausalLM

logger = logging.getLogger(__name__)

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

# Load model & processor
model_id = "microsoft/Phi-4-multimodal-instruct"

class ImageStructure:
    def __init__(self) -> None:

        # clear GPU memoery usage
        torch.cuda.empty_cache()
        torch.cuda.memory_summary(device=None, abbreviated=False)

        self.processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
        self.generation_config = GenerationConfig.from_pretrained(model_id)

        self.model = AutoModelForCausalLM.from_pretrained(
            model_id, 
            trust_remote_code=True,
            device_map="cuda", 
            torch_dtype="auto", 
            # if you do use Ampere or later GPUs, change attention to "flash_attention_2"
            _attn_implementation='eager',
        )
        
        # Move input tensors to the same device as the model
        self.device = next(self.model.parameters()).device
        
        logger.info(f"Using device: {self.device}")                

    def process(self, raw_image):
        # Prompt for transaction extraction

        user_prompt = '<|user|>'
        assistant_prompt = '<|assistant|>'
        prompt_suffix = '<|end|>'

        prompt = f"""{user_prompt}<|image_1|>Extract all transactions from this bank statement image and return them in JSON format. 
        
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
        {prompt_suffix}{assistant_prompt}

        """

        # Encode input
        inputs = self.processor(prompt, raw_image, return_tensors="pt").to('cuda:0')

        # Generate response
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=1000, generation_config=self.generation_config)

        # Decode response
        extracted_data = self.processor.decode(outputs[0], skip_special_tokens=True)

        return extracted_data

