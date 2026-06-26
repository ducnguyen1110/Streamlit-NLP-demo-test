# Project 1.1

This folder contains a few Streamlit demos for working with text and NLP ideas.

## Files

- `app.py` - a general Streamlit demo with widgets, chat UI, file upload, and session state examples.
- `app1.py` - a simple chatbot example without `session_state`.
- `app2.py` - an NLP pipeline demo for translation and spell checking.

## Setup

Create and activate a virtual environment, then install the packages you need.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install streamlit deep-translator langdetect nltk pyspellchecker langcodes
```

## Run

Start one of the apps with Streamlit:

```bash
streamlit run app.py
streamlit run app1.py
streamlit run app2.py
```

