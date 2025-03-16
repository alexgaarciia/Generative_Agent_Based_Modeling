"""
This module provides utility functions for computing similarity between agents.
It includes:
  - Numerical trait similarity (e.g., Big Five traits).
  - Text-based similarity using Sentence-BERT embeddings for 'goal' and 'ind_context'.
  - Political ideology similarity via a numeric encoding.
  
An optional language model (LLM) approach is also provided if local computations
are not desired. The weighted combination of these similarities can then be used
to identify the most similar and most different agent pairs.
"""

import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def normalize_similarity(matrix):
    """
    Normalize a cosine similarity matrix from [-1,1] to [0,1] range.

    Parameters:
        matrix (np.ndarray): A similarity matrix with values in the range [-1,1].

    Returns:
        np.ndarray: A normalized similarity matrix in the range [0,1].
    """
    return (matrix + 1) / 2  

def encode_political_ideology(ideology):
    """
    Encode a political ideology string into a numerical value.

    Parameters:
        ideology (str): The political ideology (e.g., "Liberal", "Moderate").

    Returns:
        int or None: The numeric encoding of the ideology, or None if the ideology is not recognized.
    """
    ideology_map = {
        "Liberal": 1,
        "Moderate": 2,
        "Conservative": 3,
        "Libertarian": 4,
        "Socialist": 5,
        "Anarchist": 6
    }
    return ideology_map.get(ideology)


def compute_ideology_similarity(agents):
    """
    Compute the similarity matrix for agents based on their political ideologies.

    The function converts each agent's ideology to a numerical value and then computes
    the absolute difference between every pair. These differences are normalized to produce
    a similarity score between 0 and 1 (where 1 indicates identical ideologies).

    Parameters:
        agents (list): A list of agent dictionaries containing the key "political_ideology".

    Returns:
        np.ndarray: A matrix of similarity scores between agents.
    """
    # Map each agent's political ideology to a number
    ideology_values = np.array([
        encode_political_ideology(agent["political_ideology"]) for agent in agents
    ])

    # Compute pairwise absolute differences
    ideology_similarity = np.abs(ideology_values[:, None] - ideology_values)
    
    # Normalize to a similarity score between 0 and 1
    ideology_similarity = 1 / (1 + ideology_similarity)
    return ideology_similarity


def compute_agent_similarity(agents, traits_weight=0.7, text_weight=0.15, ideology_weight=0.15, method="local"):
    """
    Compute an overall similarity matrix between agents using a weighted combination of:
      - Numerical trait similarity
      - Sentence-BERT embeddings of text (goal + context)
      - Political ideology similarity
      
    If 'method' is not "local", an LLM-based method is used instead (sends data to a language model).
    
    Parameters:
        agents (list): A list of agent dictionaries.
        traits_weight (float): Weight assigned to numerical trait similarity.
        text_weight (float): Weight assigned to text-based similarity (Sentence-BERT).
        ideology_weight (float): Weight assigned to political ideology similarity.
        method (str): "local" to compute locally; otherwise uses an LLM prompt.

    Returns:
        np.ndarray or str:
            - If method="local", returns a 2D numpy array of similarity scores.
            - Otherwise, returns the LLM response as a string.
    """
    if method == "local":
        # Extract numerical traits for each agent
        traits = np.array([
            [
                agent["traits"]["extraversion"],
                agent["traits"]["neuroticism"],
                agent["traits"]["openness"],
                agent["traits"]["conscientiousness"],
                agent["traits"]["agreeableness"],
            ]
            for agent in agents
        ])
        
        # Compute cosine similarity between agents based on traits
        traits_similarity = cosine_similarity(traits)
        traits_similarity = normalize_similarity(traits_similarity)

        # Compute text-based similarity using Sentence-BERT
        text_data = [f"{agent['goal']} {agent['ind_context']}" for agent in agents]
        model_sentence_transformer = SentenceTransformer("all-MiniLM-L6-v2")
        text_embeddings = model_sentence_transformer.encode(text_data)
        text_similarity = cosine_similarity(text_embeddings)
        text_similarity = normalize_similarity(text_similarity) 

        # Compute political ideology similarity
        ideology_similarity = compute_ideology_similarity(agents)

        # Combine all similarities using the specified weights
        combined_similarity = (
            traits_weight * traits_similarity +
            text_weight * text_similarity +
            ideology_weight * ideology_similarity
        )
        return combined_similarity
    else:
        # If not using the local method, use an LLM to compute similarity
        from simulations.concordia.language_model import mistral_model
        from simulations.concordia.language_model import gpt_model
        API_KEY = st.session_state.get("api_key", "")
        MODEL_NAME = st.session_state.get("selected_model", "")
        if MODEL_NAME == "codestral-latest":
            model = mistral_model.MistralLanguageModel(api_key=API_KEY, model_name=MODEL_NAME)
        else:
            model = gpt_model.GptLanguageModel(api_key=API_KEY, model_name=MODEL_NAME)
        
        # Construct a prompt detailing each agent's traits, goal, context, and ideology
        prompt = "Compare the following agents based on traits, goals, and ideologies:\n\n"
        for i, agent in enumerate(agents):
            prompt += f"{agent['name']}:\n"
            prompt += f"Traits: {agent['traits']}\n"
            prompt += f"Goal: {agent['goal']}\n"
            prompt += f"Context: {agent['context']}\n"
            prompt += f"Ideology: {agent['political_ideology']}\n\n"

        prompt += (
            f"The importance weights for comparison are:\n"
            f"- Traits Weight: {traits_weight}\n"
            f"- Text Weight: {text_weight}\n"
            f"- Ideology Weight: {ideology_weight}\n\n"
            "Using these weights, identify the two most similar agents and the two most different agents without giving any explanations.\n"
            "Respond in this format:\n"
            "Most Similar: Agent X, Agent Y\n"
            "Most Different: Agent A, Agent B\n"
        )

        # Generate and return the response from the language model
        text = model.sample_text(prompt)
        return text
    

def find_extreme_agents(similarity_matrix, agents):
    """
    Identify the pair of agents with the highest similarity and the pair with the lowest similarity.

    This function iterates over all unique agent pairs, comparing their similarity scores
    from the provided similarity matrix.

    Parameters:
        similarity_matrix (np.ndarray): A 2D numpy array containing pairwise similarity scores.
        agents (list): A list of agent dictionaries (used to infer the number of agents).

    Returns:
        tuple: Two tuples:
            - The indices of the two most similar agents.
            - The indices of the two most different agents.
    """
    # Total number of agents
    num_agents = len(agents)  
    
    # Initialize maximum similarity to a very low value
    max_similarity = -1       
    
    # Initialize minimum similarity to a very high value
    min_similarity = float('inf')  
    most_similar_pair = ()
    most_different_pair = ()

    # Iterate over each unique pair of agents
    for i in range(num_agents):
        for j in range(i + 1, num_agents):
            similarity = similarity_matrix[i, j]
            # Update the most similar pair if a higher similarity is found
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_pair = (i, j)
            # Update the most different pair if a lower similarity is found
            if similarity < min_similarity:
                min_similarity = similarity
                most_different_pair = (i, j)
    
    return most_similar_pair, most_different_pair
