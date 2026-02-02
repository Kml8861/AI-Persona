from transformers import AutoTokenizer

class TokenCounter:
        def __init__(self, model_name= "mistralai/Mistral-7B-v0.1"):
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)

        def count_text(self, text: str) -> int:
            return len(self.tokenizer.encode(text))

        def count_message_accurate(self, msg: dict) -> int:
            combined = f"{msg['role']}: {msg['content']}\n"
            return self.count_text(combined)

        def count_message_fast(self, msg: dict) -> int:
            return self.count_text(msg["content"]) + 4