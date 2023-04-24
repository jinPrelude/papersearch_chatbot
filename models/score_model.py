import openai


class ScoreModel:
    def __init__(self):
        self.conversation_history = []
        self.model = "gpt-3.5-turbo"
        self.temperature = 0.0
        self.max_tokens = 1

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
        return int(response.choices[0].message.content)

    def _get_prompt(self, message):
        prompt = """
        You are an AI that analyzes the user's sentence and determines whether the user wants to find the research article, 
        returning a 1 if they do, or a 0 if they don't. Your judgment is based on the following criteria:
        1. determine if the researcher wants to find relevant research materials, not just ask for information.
        2. the sentence should be clear enough to understand what kind of research data the researcher wants to find.
        you should output only the score, not the sentence.
        
        example :
        input: "I want to know about <something>", result : 0
        input: "what is <something>", result : 0
        input: "find some reference for <something>", result : 1
        input: "is there any research about <something>", result : 1
        input: "Can you recommend just one of the papers you recommended? ", result : 0
        input: " 
        """
        prompt += message
        prompt += """
        ", result : "
        """
        messages = [{"role": "system", "content": prompt}]
        return messages
