# File: gpt4all_expander/context_manager.py

from gpt4all import GPT4All
import logging

class ContextManager:
    def __init__(self, model_path):
        self.model = GPT4All(model_path)
        self.current_context = []

    def update_context(self, new_text):
        self.current_context.append(new_text)

    def generate(self, prompt, min_tokens=100, max_retries=10, **kwargs):
        full_prompt = '\n'.join(self.current_context + [prompt])
        for i in range(max_retries):
            adjusted_max_tokens = min_tokens + (i * 50)  # Adjusted this line
            response = self.model.generate(full_prompt, max_tokens=adjusted_max_tokens, **kwargs)
            if len(response.split()) >= min_tokens:
                return response
        logging.error(f"Unable to generate response with minimum {min_tokens} tokens after {max_retries} retries.")
        raise ValueError(f"Unable to generate response with minimum {min_tokens} tokens after {max_retries} retries.")
