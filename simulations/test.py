from agent_similarity import compute_agent_similarity
from concordia.language_model import mistral_model
import streamlit as st

import json
with open('../agents.json', 'r') as f:
    agents = json.load(f)

API_KEY = ""
MODEL_NAME = "codestral-latest"
model = mistral_model.MistralLanguageModel(api_key=API_KEY, model_name=MODEL_NAME)


# Prepare a prompt for the LLM
prompt = "Compare the following agents based on traits, goals, and ideologies:\n\n"
for i, agent in enumerate(agents):
    prompt += f"{agent['name']}:\n"
    prompt += f"Traits: {agent['traits']}\n"
    prompt += f"Goal: {agent['goal']}\n"
    prompt += f"Context: {agent['context']}\n"
    prompt += f"Ideology: {agent['political_ideology']}\n\n"

prompt += (
            "Identify the two most similar agents and the two most different agents.\n"
            "Return your answer in this JSON format, RESTRICT TO THIS, DO NOT RETURN ANYTHING ELSE: { 'most_similar': ['Agent X', 'Agent Y'], 'most_different': ['Agent A', 'Agent B'] }")

text2 = compute_agent_similarity(agents, method="llm")
st.write(text2)
#similarity_result = json.loads(text2)
#most_similar = similarity_result.get("most_similar", [])
#most_different = similarity_result.get("most_different", [])
#st.write(most_similar)
