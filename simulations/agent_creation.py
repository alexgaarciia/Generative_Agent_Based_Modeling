"""
This module provides utility functions for validating agent structures and generating generic knowledge 
for simulation participants. It includes functions for validating the format of agent JSON files, ensuring 
that agents have the required attributes and correct data types. Additionally, it provides a function to 
generate a concise summary of a shared context using a language model.
"""

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
    "traits": {
        "extraversion": int,
        "neuroticism": int,
        "openness": int,
        "conscientiousness": int,
        "agreeableness": int
    },
    "formative_ages": list
}

def validate_agent(agent):
    """
    Validates that the provided agent dictionary matches to the expected format.

    This function checks for:
      - 'name', 'gender', and 'political_ideology' are strings.
      - 'traits' is a dictionary with integer values.
      - 'formative_ages' is a list of integers.

    Parameters:
        agent (dict): The agent data to validate.

    Returns:
        bool: True if the agent matches the expected structure, False otherwise.
    """
    try:
        # Check basic string fields
        if not isinstance(agent["name"], str):
            return False
        if not isinstance(agent["gender"], str):
            return False
        if not isinstance(agent["political_ideology"], str):
            return False

        # Check that all trait values are integers
        traits = agent["traits"]
        if not all(isinstance(traits[key], int) for key in traits):
            return False

        # Check that formative ages is a list of integers
        if not isinstance(agent["formative_ages"], list):
            return False
        if not all(isinstance(age, int) for age in agent["formative_ages"]):
            return False

        return True
    except KeyError:
        # A missing key indicates the agent structure is invalid
        return False
    

def validate_agents_file(uploaded_file):
    """
    Validates the structure of an uploaded JSON file containing agents.

    The function ensures:
      - The file contains a JSON list.
      - Each agent in the list adheres to the expected structure.

    Parameters:
        uploaded_file: A file object or already-parsed JSON data.

    Returns:
        tuple: A tuple (bool, str) where the boolean indicates whether the file is valid,
               and the string provides a message regarding the validation result.
    """
    try:
        # Load JSON content from the file if needed
        agents_data = json.load(uploaded_file) if hasattr(uploaded_file, 'read') else uploaded_file

        # Check that the JSON data is a list
        if not isinstance(agents_data, list):
            return False, "The uploaded file must be a list of agents."

        # Validate each agent in the list
        for agent in agents_data:
            if not validate_agent(agent):
                return False, f"Agent {agent.get('name', 'Unnamed')} has an invalid structure."

        return True, "The uploaded file is valid."
    except json.JSONDecodeError:
        return False, "The uploaded file is not a valid JSON."
    except Exception as e:
        return False, str(e)


def create_generic_knowledge(shared_memories):
    """
    Generates a summarized version of shared context for simulation participants.

    This function retrieves the shared context from the session state,
    creates a prompt, and uses the language model to generate a concise summary.

    Parameters:
        shared_memories: Not used directly; the function accesses the shared context via session state.

    Returns:
        str: The summarized shared context.
    """
    # Build a prompt and generate a summary using the language model.
    shared_context = model.sample_text(
        'Summarize the following passage in a concise and insightful fashion:\n'
        + '\n'.join(shared_memories)
        + '\n'
        + 'Summary:'
    )
    return shared_context
