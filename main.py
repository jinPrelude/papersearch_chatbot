import os
from typing import Dict, Tuple, List

import openai

from crawler import ElicitSearchDriver
from models import SearchQueryModel, ScoreModel, GPT3ChatModel
from models.utils import HistoryHolder

openai.api_key = os.environ["OPENAI_API_KEY"]


class Pipeline:
    def __init__(
        self,
        history: HistoryHolder,
        search_driver: ElicitSearchDriver,
        query_model: SearchQueryModel,
        score_model: ScoreModel,
        chat_model: GPT3ChatModel,
    ):
        self.history = history
        self.search_driver = search_driver
        self.query_model = query_model
        self.score_model = score_model
        self.chat_model = chat_model

    def generate_prompt(self, message: str, history: str, score: int, result_dict: str) -> List[Dict[str, str]]:
        prompt = f"You are DeepSight, an AGI research assistant. user: {message}\n"

        if score == 1:
            prompt += (
                f"search result based on user's message: {result_dict}.\n"
                f"Introduce and rank up to three of the most relevant papers for user."
            )

        prompt += f"chat history: [{history}]\nDeepSight : "
        messages = [{"role": "assistant", "content": prompt}]

        return messages

    def run(self, user_input: str) -> Tuple[str, Dict[str, any]]:
        infos = {"score": 0}
        score = self.score_model.get_score(user_input)
        infos["score"] = score

        if score == 1:
            query = self.query_model.get_score(user_input)
            search_result = self.search_driver.search(query)
            infos.update({"query": query, "search_result": search_result})

        search_result_str = str(infos.get("search_result", "")).replace("\'", "")
        prompt = self.generate_prompt(user_input, self.history.return_str(), score, search_result_str)
        response = self.chat_model.generate_response(prompt)

        return response, infos


def main():
    elicit = ElicitSearchDriver()
    query_model = SearchQueryModel()
    score_model = ScoreModel()
    chat_model = GPT3ChatModel()
    history = HistoryHolder(max_word_len=512)

    pipeline = Pipeline(history, elicit, query_model, score_model, chat_model)

    while True:
        message = input("User: ")
        response, infos = pipeline.run(message)
        history.append(user=message, ai_response=response)
        print(f"AI: {response}")


if __name__ == "__main__":
    main()
