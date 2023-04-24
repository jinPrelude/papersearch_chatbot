import openai


class ScoreModel:
    def __init__(self):
        self.conversation_history = []
        self.model = "gpt-3.5-turbo"
        self.temperature = 0.0
        self.max_tokens = 1

    def get_score(self, prompt):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        return int(response.choices[0].message.content)

    def get_prompt(self, message, chat_history):
        prompt = (
        "You are an AI that analyzes the user\'s chat history and determines whether the user wants to find the research article, returning a 1 if they do, or a 0 if they don\'t. Your judgment is based on the following criteria:\n"
        "1. determine if the researcher wants to find relevant research, not just ask for information.\n"
        "2. the sentence should be clear enough to understand what kind of research data the researcher wants to find.\n"
        "you should output only the score, no any other sentence.\n"
        )
        prompt += f"chat history: <start>{chat_history}<end>\n"
        prompt += (
            "example :\n"
            "input: I want to know about <something>, result : 0\n"
            "input: what is <something>, result : 0\n"
            "input: find some reference for <something>, result : 1\n"
            "input: is there any research about <something>, result : 1\n"
            "input: Can you recommend just one of the papers you recommended?, result : 0\n"
        )
        prompt += f"input: {message}, result: "
        messages = [{"role": "system", "content": prompt}]
        return messages

    def run(self, message: str, chat_history: str) -> int:
        prompt = self.get_prompt(message, chat_history)
        return self.get_score(prompt)