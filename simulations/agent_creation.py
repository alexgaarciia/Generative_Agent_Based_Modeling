import json
import streamlit as st
from simulations.concordia.language_model import gpt_model
from simulations.concordia.language_model import mistral_model


# Setup LLM
API_KEY = st.session_state.get("api_key", "")
MODEL_NAME = st.session_state.get("selected_model", "")
if MODEL_NAME == "codestral-latest":
    model = mistral_model.MistralLanguageModel(api_key=API_KEY, model_name=MODEL_NAME)
else:
    model = gpt_model.GptLanguageModel(api_key=API_KEY, model_name=MODEL_NAME)


# Define the expected structure of the agent
expected_agent_structure = {
    "name": str,
    "gender": str,
    "political_ideology": str,
    "goal": str,
    "context": str,
    "traits": {
        "extraversion": int,
        "neuroticism": int,
        "openness": int,
        "conscientiousness": int,
        "agreeableness": int
    },
    "formative_ages": list
}


# Validate if the agent matches the expected format
def validate_agent(agent):
    try:
        # Validate basic structure of the agent
        if not isinstance(agent["name"], str):
            return False
        if not isinstance(agent["gender"], str):
            return False
        if not isinstance(agent["political_ideology"], str):
            return False
        if not isinstance(agent["goal"], str):
            return False
        if not isinstance(agent["context"], str):
            return False
        
        # Validate traits
        traits = agent["traits"]
        if not all(isinstance(traits[key], int) for key in traits):
            return False

        # Validate formative ages
        if not isinstance(agent["formative_ages"], list):
            return False
        if not all(isinstance(age, int) for age in agent["formative_ages"]):
            return False
        
        return True
    except KeyError:
        return False
    

# Validate if the uploaded JSON file follows the correct structure
def validate_agents_file(uploaded_file):
    try:
        # Read content if it's a file object
        agents_data = json.load(uploaded_file) if hasattr(uploaded_file, 'read') else uploaded_file
        
        # Check if the uploaded JSON is a list of agents
        if not isinstance(agents_data, list):
            return False, "The uploaded file must be a list of agents."
        
        # Check if each agent follows the expected format
        for agent in agents_data:
            if not validate_agent(agent):
                return False, f"Agent {agent.get('name', 'Unnamed')} has an invalid structure."

        return True, "The uploaded file is valid."
    except json.JSONDecodeError:
        return False, "The uploaded file is not a valid JSON."
    except Exception as e:
        return False, str(e)


# Configure the generic knowledge of players and GM
def create_generic_knowledge(shared_memories):
    shared_memories = st.session_state["shared_context"]
    shared_context = model.sample_text(
        'Summarize the following passage in a concise and insightful fashion:\n'
        + '\n'.join(shared_memories)
        + '\n'
        + 'Summary:'
    )
    return shared_context
