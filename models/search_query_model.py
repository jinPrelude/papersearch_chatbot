import openai


class SearchQueryModel:
    def __init__(self):
        self.conversation_history = []
        self.model = "gpt-3.5-turbo"
        self.temperature = 0.0
        self.max_tokens = 256

    def get_score(self, message):
        prompt = self._get_prompt(message)
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        return response.choices[0].message.content

    def _get_prompt(self, message):
        prompt = """
        You are an artificial intelligence that turns user sentences into queries. The user will ask you to find research on a specific topic. Analyze the user's sentence and translate it into a search query that will best yield the research the user wants.
        
        here's the example :
        input: "find some reference that used attention model for solving reinforcement learning task", result : reinforcement learning transformer attention
        input: "is there a research that used gnn for NLP?", result : graph neural network natural language processing
        input: "Can you find a paper that is aimed for enhancing memorizing performance of transformer?", result : transformer memory
        input: " 
        """
        prompt += message
        prompt += """
        ", result : 
        """
        messages = [{"role": "system", "content": prompt}]
        return messages
