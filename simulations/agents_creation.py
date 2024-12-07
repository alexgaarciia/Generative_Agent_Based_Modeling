# Import necessary libraries and components
import random
import sentence_transformers
import streamlit as st
from concordia.language_model import gpt_model

# Setup sentence encoder
st_model = sentence_transformers.SentenceTransformer(
    'sentence-transformers/all-mpnet-base-v2')
embedder = lambda x: st_model.encode(x, show_progress_bar=False)

# Setup LLM
GPT_API_KEY = st.session_state.get("api_key", "")
GPT_MODEL_NAME = st.session_state.get("selected_model", "")
model = gpt_model.GptLanguageModel(api_key=GPT_API_KEY, model_name=GPT_MODEL_NAME)

# Agent configuration
def make_random_formative_ages():
    return sorted(random.sample(range(5, 40), 5))
