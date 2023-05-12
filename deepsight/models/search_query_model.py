import openai


class SearchQueryModel:
    def __init__(self):
        self.conversation_history = []
        self.model = "gpt-3.5-turbo"
        self.temperature = 0.0
        self.max_tokens = 256

    def get_query(self, prompt):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        return response.choices[0].message.content

    def get_prompt(self, message: str, chat_history: str) -> str:
        prompt = "You are an artificial intelligence that turns user sentences into queries. The user will ask you to find research on a specific topic. Analyze the user's sentence and translate it into a search query that will best yield the research the user wants.\n"
        prompt += f"chat history: <start>{chat_history}<end>\n"
        prompt += (
            "here's the example :\n"
            "input: find some reference that used attention model for solving reinforcement learning task, result : reinforcement learning transformer attention\n"
            "input: is there a research that used gnn for NLP?, result : graph neural network natural language processing\n"
            "input: Can you find a paper that is aimed for enhancing memorizing performance of transformer?, result : transformer memory\n"
        )
        prompt += f"input: {message}, result: "
        messages = [{"role": "system", "content": prompt}]
        return messages

    def run(self, message: str, chat_history: str) -> str:
        prompt = self.get_prompt(message, chat_history)
        return self.get_query(prompt)
