import openai

from typing import Dict, List

class GPT3ChatModel:
    def __init__(self, max_tokens: int = 256):
        self.conversation_history = []
        self.model = "gpt-3.5-turbo"
        self.temperature = 0.0
        self.max_tokens = max_tokens

    def get_prompt(self, message: str, history: str, score: int, result_dict: str) -> List[Dict[str, str]]:
        prompt = f"You are DeepSight, an AGI research assistant. user: {message}\n"

        if score == 1:
            prompt += (
                f"search result based on user's message: {result_dict}.\n"
                f"Introduce and rank up to three papers base on the relevance between user's request, paper's title and abstract.\n"
                "template for paper info : [title] by [authors]([publication_year], [citation])-[summary]\n"
            )

        prompt += f"chat history: [{history}]\nDeepSight : "
        messages = [{"role": "assistant", "content": prompt}]

        return messages

    def get_response(self, prompt: str):
        print(f"receiving response...", end=" ")
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        print("done!")
        return response.choices[0].message.content

    def run(self, message: str, history: str, score: int, search_resul_str: str) -> str:
        prompt = self.get_prompt(message, history, score, search_resul_str)
        return self.get_response(prompt)
