# PaperSearch Chatbot
[PaperSearch Chatbot](#) is a chatbot that can help you find papers related to based on your request. It uses ChatGPT for chatbot model, and [Elicit](https://elicit.org), a search engine for scientific papers using GPT3. 

![ezgif com-video-to-gif](https://github.com/jinPrelude/papersearch_chatbot/assets/16518993/b4e62c61-41a2-42a1-9c4e-77f93ab39a57)


## Installation
We use [poetry](https://python-poetry.org) for dependency management:
```bash
pip install poetry
poetry install
```

## Usage
### Add your API key & Elicit account info
You need to add your OPENAI_API_KEY and [Elicit account](https://elicit.org/signup) info in `.env.template` file:
```bash
OPENAI_API_KEY = your_openai_api_key

# Elicit
ELICIT_EMAIL = your_elicit_email
ELICIT_PASSWORD = your_elicit_password
```
NOTE : you should Sign up Elicit using email.

### Run chatbot

This project used [Gradio](https://gradio.app), a python library for quickly creating UIs for your machine learning model.
```bash
python run_gradio.py
```
By running run_gradio.py file, you can get local URL for using chatbot.


## Architecture
![필요그림자료 005](https://github.com/jinPrelude/papersearch_chatbot/assets/16518993/44a56489-a763-4db1-8071-bdd15d8ae81a)