import os

import gradio as gr
import openai
from dotenv import load_dotenv

from crawler import ElicitSearchDriver
from models import SearchQueryModel, ScoreModel, GPT3ChatModel
from models.utils import HistoryHolder
from pipeline import Pipeline


load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]


def main():

    with gr.Blocks() as demo:
        elicit = ElicitSearchDriver()
        query_model = SearchQueryModel()
        score_model = ScoreModel()
        chat_model = GPT3ChatModel()
        history = HistoryHolder(max_word_len=512)
        pipeline = Pipeline(history, elicit, query_model, score_model, chat_model)

        chatbot = gr.Chatbot()
        msg = gr.Textbox()
        clear = gr.Button("Clear")

        def respond(message, chat_history):
            bot_message, _ = pipeline.run(message)
            chat_history.append((message, bot_message))
            history.append(user=message, ai_response=bot_message)
            return "", chat_history

        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        clear.click(lambda: None, None, chatbot, queue=False)

    demo.launch(share=False)


if __name__ == "__main__":
    main()

