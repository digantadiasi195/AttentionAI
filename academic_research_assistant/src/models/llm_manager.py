# src/models/llm_manager.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from ..config import Config

class LLMManager:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(
            Config.MODEL_NAME,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
    def generate_response(self, prompt, max_length=500):
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        outputs = self.model.generate(
            **inputs,
            max_length=max_length,
            num_return_sequences=1,
            temperature=0.7,
            do_sample=True
        )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
        
    def summarize_papers(self, papers):
        # Create a prompt for summarization
        prompt = "Summarize the following research papers and their key contributions:\n\n"
        for paper in papers:
            prompt += f"Title: {paper['title']}\nAbstract: {paper['abstract']}\n\n"
        
        return self.generate_response(prompt, max_length=1000)
    
    def answer_question(self, question, papers):
        # Create a prompt for Q&A
        prompt = f"Based on the following research papers, answer this question: {question}\n\n"
        for paper in papers:
            prompt += f"Title: {paper['title']}\nAbstract: {paper['abstract']}\n\n"
        
        return self.generate_response(prompt)
    
    def generate_future_directions(self, papers):
        prompt = """Based on these papers, suggest future research directions and improvements:
        
        Papers:
        """
        for paper in papers:
            prompt += f"Title: {paper['title']}\nAbstract: {paper['abstract']}\n\n"
        
        return self.generate_response(prompt, max_length=1500)