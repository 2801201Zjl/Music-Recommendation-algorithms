import torch
from transformers import AutoTokenizer, AutoModel

class LLMProcessor:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
        self.model = AutoModel.from_pretrained("bert-base-chinese")

    def process_text(self, texts):
        """处理文本数据，提取语义特征"""
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1)

def process_text(comments):
    processor = LLMProcessor()
    return processor.process_text(comments) 