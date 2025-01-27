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


# Download necessary NLTK data files
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


def get_wordnet_pos(word):
    # Map NLTK part-of-speech tags to WordNet tags for accurate lemmatization
    tag = nltk.pos_tag([word])[0][1][0].upper()  # Get the first letter of POS tag and capitalize it
    tag_dict = {
        "J": wn.ADJ,
        "N": wn.NOUN,
        "V": wn.VERB,
        "R": wn.ADV,
    }
    return tag_dict.get(tag, wn.NOUN)


def clean_text(text, stopwords_en, wnl):
    # Clean and preprocess text for better TF-IDF representation
    text = contractions.fix(text)  # Expand contractions
    text = re.sub(r'\d+', '', text)  # Remove numbers
    tokens = [token for token in wordpunct_tokenize(text) if token.isalnum()]  # Tokenization
    tokens = [wnl.lemmatize(token.lower(), get_wordnet_pos(token)) for token in tokens]  # Lemmatization
    tokens = [token for token in tokens if token not in stopwords_en]  # Remove stopwords
    return " ".join(tokens)


def preprocess_single_agent(agent, stopwords_en, wnl):
    # Preprocess the goal and context of a single agent
    if "goal" in agent:
        agent["goal"] = clean_text(agent["goal"], stopwords_en, wnl)
    if "context" in agent:
        agent["context"] = clean_text(agent["context"], stopwords_en, wnl)
    return agent


def preprocess_text_data(agents):
    # Preprocess all agents using parallel processing
    stopwords_en = set(stopwords.words("english"))  # Load the set of English stopwords
    wnl = WordNetLemmatizer()  # Initialize a lemmatizer

    # Parallelize the preprocessing of agents
    processed_agents = Parallel(n_jobs=-1)(
        delayed(preprocess_single_agent)(agent, stopwords_en, wnl) for agent in agents
    )
    return processed_agents


def encode_political_ideology(ideology):
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
    # Convert ideologies to numerical values
    ideology_values = np.array([
        encode_political_ideology(agent["political_ideology"]) for agent in agents
    ])

    # Compute absolute pairwise differences in ideology values (smaller distance means more similar)
    ideology_similarity = np.abs(ideology_values[:, None] - ideology_values)

    # Normalize differences to a similarity score in the range [0, 1]
    ideology_similarity = 1 / (1 + ideology_similarity) 
    return ideology_similarity


def compute_agent_similarity(agents, traits_weight=0.7, text_weight=0.15, ideology_weight=0.15, method="local"):
    if method == "local":
        # Preprocess text data
        agents = preprocess_text_data(agents)
        # st.write(agents)

        # Extract numerical traits 
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

        # Compute cosine similarity for traits
        traits_similarity = cosine_similarity(traits)

        # Combine text data into a single string
        text_data = [f"{agent['goal']} {agent['context']}" for agent in agents]

        # Compute the TF-IDF matrix for text data
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(text_data)

        # Calculate cosine similarity for text data
        text_similarity = cosine_similarity(tfidf_matrix)
        # st.write(text_similarity)

        # Compute political ideology similarity
        ideology_similarity = compute_ideology_similarity(agents)
        # st.write(ideology_similarity)

        # Combine similarities with a weighted average
        combined_similarity = (
            traits_weight * traits_similarity +
            text_weight * text_similarity +
            ideology_weight * ideology_similarity
        )
        return combined_similarity
    else:
        from simulations.concordia.language_model import mistral_model
        from simulations.concordia.language_model import gpt_model
        API_KEY = st.session_state.get("api_key", "")
        MODEL_NAME = st.session_state.get("selected_model", "")
        if MODEL_NAME == "codestral-latest":
            model = mistral_model.MistralLanguageModel(api_key=API_KEY, model_name=MODEL_NAME)
        else:
            model = gpt_model.GptLanguageModel(api_key=API_KEY, model_name=MODEL_NAME)
        
        # Prepare a prompt for the LLM
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

        text = model.sample_text(prompt)
        return text
    

def find_extreme_agents(similarity_matrix, agents):
    # Total number of agents
    num_agents = len(agents)  

    # Initialize max similarity as a very low value
    max_similarity = -1

    # Initialize min similarity as a very high value
    min_similarity = float('inf')
    most_similar_pair = ()
    most_different_pair = ()

    # Iterate through all unique pairs of agents
    for i in range(num_agents):
        for j in range(i+1 , num_agents):  # Only consider unique pairs
            similarity = similarity_matrix[i, j]  # Extract similarity score
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_pair = (i, j)
            if similarity < min_similarity:
                min_similarity = similarity
                most_different_pair = (i, j)
    
    return most_similar_pair, most_different_pair
