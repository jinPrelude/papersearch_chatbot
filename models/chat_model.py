import openai


class GPT3ChatModel:
    def __init__(self, max_tokens: int = 256):
        self.conversation_history = []
        self.model = "gpt-3.5-turbo"
        self.temperature = 0.0
        self.max_tokens = max_tokens

    def generate_response(self, prompt):
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
