"""
This module provides utility functions for cleaning, preprocessing, and computing similarity between agents.
It includes text normalization using NLTK and contractions, TF-IDF vectorization for text-based similarity,
and cosine similarity computations for numerical traits and political ideologies.
Parallel processing is employed to speed up text preprocessing.
"""

import re
import nltk
import numpy as np
import contractions
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords, wordnet as wn
from joblib import Parallel, delayed

# -----------------------------------------------------------------------------
# Download necessary NLTK data files if not already present.
# -----------------------------------------------------------------------------
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


def get_wordnet_pos(word):
    """
    Map an NLTK part-of-speech tag to a WordNet POS tag for accurate lemmatization.

    Parameters:
        word (str): The word for which the POS tag is to be determined.

    Returns:
        str: The corresponding WordNet POS tag (e.g., wn.NOUN, wn.VERB). 
             Defaults to wn.NOUN if no mapping is found.
    """
    # Get the POS tag for the word and extract the first letter of the tag
    tag = nltk.pos_tag([word])[0][1][0].upper()
    
    # Define mapping from NLTK POS tag initial to WordNet POS tag
    tag_dict = {
        "J": wn.ADJ,
        "N": wn.NOUN,
        "V": wn.VERB,
        "R": wn.ADV,
    }
    return tag_dict.get(tag, wn.NOUN)


def clean_text(text, stopwords_en, wnl):
    """
    Clean and preprocess a text string for improved TF-IDF representation.

    The cleaning process includes:
      - Expanding contractions.
      - Removing numerical digits.
      - Tokenizing the text into alphanumeric tokens.
      - Converting tokens to lowercase and lemmatizing them based on POS.
      - Removing stopwords.

    Parameters:
        text (str): The raw text string to be cleaned.
        stopwords_en (set): A set of English stopwords to be removed.
        wnl (WordNetLemmatizer): An instance of a WordNet lemmatizer.

    Returns:
        str: The cleaned and preprocessed text.
    """
    # Expand contractions 
    text = contractions.fix(text)  
    
    # Remove all numeric characters
    text = re.sub(r'\d+', '', text)  
    
    # Tokenize the text and retain only alphanumeric tokens
    tokens = [token for token in wordpunct_tokenize(text) if token.isalnum()]
    
    # Lowercase and lemmatize each token using the appropriate POS tag
    tokens = [wnl.lemmatize(token.lower(), get_wordnet_pos(token)) for token in tokens]
    
    # Remove any stopwords from the token list
    tokens = [token for token in tokens if token not in stopwords_en]
    return " ".join(tokens)


def preprocess_single_agent(agent, stopwords_en, wnl):
    """
    Preprocess the 'goal' and 'context' fields of a single agent.

    Parameters:
        agent (dict): A dictionary representing an agent, expected to contain keys 'goal' and 'context'.
        stopwords_en (set): A set of English stopwords.
        wnl (WordNetLemmatizer): An instance of WordNetLemmatizer for lemmatization.

    Returns:
        dict: The updated agent dictionary with cleaned 'goal' and 'context' fields.
    """
    if "goal" in agent:
        agent["goal"] = clean_text(agent["goal"], stopwords_en, wnl)
    if "context" in agent:
        agent["context"] = clean_text(agent["context"], stopwords_en, wnl)
    return agent


def preprocess_text_data(agents):
    """
    Preprocess the textual data (goal and context) for a list of agents using parallel processing.

    This function initializes necessary resources (stopwords and lemmatizer) and then processes each agent in parallel.

    Parameters:
        agents (list): A list of agent dictionaries.

    Returns:
        list: The list of processed agent dictionaries with updated text fields.
    """
    # Load English stopwords and initialize the WordNet lemmatizer
    stopwords_en = set(stopwords.words("english"))
    wnl = WordNetLemmatizer()

    # Use parallel processing to preprocess each agent concurrently
    processed_agents = Parallel(n_jobs=-1)(
        delayed(preprocess_single_agent)(agent, stopwords_en, wnl) for agent in agents
    )
    return processed_agents


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
    Compute the overall similarity matrix between agents using weighted components.

    Two methods are available:
      - "local": Uses local computations to derive similarities based on numerical traits,
                 TF-IDF representations of textual data, and political ideology.
      - Otherwise: Uses a language model (LLM) to compute similarities by comparing agents
                     via a generated prompt.

    Parameters:
        agents (list): A list of agent dictionaries.
        traits_weight (float): Weight assigned to the similarity of numerical traits.
        text_weight (float): Weight assigned to text-based similarity.
        ideology_weight (float): Weight assigned to political ideology similarity.
        method (str): The method to compute similarity ("local" for local functions or any other value for LLM-based).

    Returns:
        np.ndarray or str: If using the "local" method, returns a similarity matrix (numpy array).
                           Otherwise, returns the response from the language model.
    """
    if method == "local":
        # Preprocess the textual data for each agent
        agents = preprocess_text_data(agents)
        
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

        # Combine 'goal' and 'context' fields for text processing
        text_data = [f"{agent['goal']} {agent['context']}" for agent in agents]
        
        # Vectorize the text using TF-IDF
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(text_data)
        
        # Compute cosine similarity on the TF-IDF matrix
        text_similarity = cosine_similarity(tfidf_matrix)

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
