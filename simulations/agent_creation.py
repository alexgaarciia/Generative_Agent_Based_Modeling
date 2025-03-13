"""
This module provides utility functions and form logic for creating and validating agents, as well as 
generating shared context summaries. It includes:

- A function to display a Streamlit form for agent creation, collecting information on personal details 
  and personality traits.
- Validation functions for checking the structure and data types within agent JSON files.
- A function for producing concise summaries of shared context using a language model.
"""

import json
import random
import streamlit as st
from simulations.concordia.language_model import gpt_model
from simulations.concordia.language_model import mistral_model

# LLM Setup
API_KEY = st.session_state.get("api_key", "")
MODEL_NAME = st.session_state.get("selected_model", "")
if MODEL_NAME == "codestral-latest":
    model = mistral_model.MistralLanguageModel(api_key=API_KEY, model_name=MODEL_NAME)
else:
    model = gpt_model.GptLanguageModel(api_key=API_KEY, model_name=MODEL_NAME)

def create_agent(num_agents):
    """
    Displays a Streamlit form to create or edit details for one agent, storing the result in session state.

    This function:
      - Shows input fields for the agent's name, gender, political ideology, and Big Five traits.
      - Randomly generates a list of formative ages.
      - Appends the newly created agent to the session state (`st.session_state["agents"]`).
      - Increments the `st.session_state["current_agent"]` counter until it reaches `num_agents`.
      - Sets `st.session_state["form_submitted"]` to True once all agents have been created.

    Parameters:
        num_agents (int): Total number of agents to be created.

    Returns:
        None. Results are saved in `st.session_state`.
    """
    agent_index = st.session_state.current_agent

    with st.form(key=f"agent_form_{agent_index}"):
        st.markdown(f"## **Agent {agent_index + 1}**")
        name = st.text_input(f"Name of Agent {agent_index + 1}:")
        gender = st.selectbox(
            f"Gender of Agent {agent_index + 1}:", options=["Male", "Female"]
        )
        political_ideology = st.selectbox(
            f"Political Ideology of Agent {agent_index + 1}:",
            options=["Liberal", "Conservative", "Moderate",
                     "Libertarian", "Socialist", "Anarchist"]
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"#### Big Five Personality Traits for Agent {agent_index + 1}:")
        extraversion = st.selectbox("Extraversion", [1, 2, 3, 4, 5])
        neuroticism = st.selectbox("Neuroticism", [1, 2, 3, 4, 5])
        openness = st.selectbox("Openness", [1, 2, 3, 4, 5])
        conscientiousness = st.selectbox("Conscientiousness", [1, 2, 3, 4, 5])
        agreeableness = st.selectbox("Agreeableness", [1, 2, 3, 4, 5])
        formative_ages = sorted(random.sample(range(5, 40), 5))

        submit_button = st.form_submit_button(label="Save Agent", use_container_width=True)

        if submit_button:
            agent = {
                "name": name,
                "gender": gender,
                "political_ideology": political_ideology,
                "traits": {
                    'extraversion': extraversion,
                    'neuroticism': neuroticism,
                    'openness': openness,
                    'conscientiousness': conscientiousness,
                    'agreeableness': agreeableness,
                },
                "formative_ages": formative_ages,
            }
            st.session_state.agents.append(agent)

            if agent_index < num_agents - 1:
                st.session_state.current_agent += 1
                st.warning("Verify agent's details")
            else:
                st.session_state.form_submitted = True

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
