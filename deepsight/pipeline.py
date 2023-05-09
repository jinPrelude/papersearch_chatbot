from typing import Dict, Tuple, List

from deepsight.crawler import ElicitSearchDriver
from deepsight.models import SearchQueryModel, ScoreModel, GPT3ChatModel
from deepsight.models.utils import HistoryHolder



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


    def run(self, user_input: str) -> Tuple[str, Dict[str, any]]:
        infos = {"score": 0}
        chat_history = self.history.return_str()

        score = self.score_model.run(user_input, chat_history)
        infos["score"] = score

        if score == 1:
            query = self.query_model.run(user_input, chat_history)
            search_result = self.search_driver.search(query)
            infos.update({"query": query, "search_result": search_result})

        search_result_str = str(infos.get("search_result", "")).replace("\'", "")
        response = self.chat_model.run(user_input, self.history.return_str(), score, search_result_str)

        return response, infos