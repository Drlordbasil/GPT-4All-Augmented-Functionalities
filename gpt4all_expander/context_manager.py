# File: gpt4all_expander/context_manager.py

from gpt4all import GPT4All
import logging

class ContextManager:
    def __init__(self, model_path: str):
        self.model = GPT4All(model_path)
        self.current_context = []

    def update_context(self, new_text: str) -> None:
        self.current_context.append(new_text)

    def generate(self, prompt: str, min_tokens: int = 100, max_retries: int = 10, **kwargs) -> str:
        full_prompt = '\n'.join(self.current_context + [prompt])
        for i in range(max_retries):
            adjusted_max_tokens = min_tokens + (i * 50)
            response = self.model.generate(full_prompt, max_tokens=adjusted_max_tokens, **kwargs)
            if len(response.split()) >= min_tokens:
                return response
        logging.error(f"Unable to generate response with minimum {min_tokens} tokens after {max_retries} retries.")
        raise ValueError(f"Unable to generate response with minimum {min_tokens} tokens after {max_retries} retries.")

