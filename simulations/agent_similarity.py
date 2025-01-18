import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


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
    ideology_values = np.array([
        encode_political_ideology(agent["political_ideology"]) for agent in agents
    ])

    # Calculate ideological distances (smaller distanc means more similar)
    ideology_similarity = np.abs(ideology_values[:, None] - ideology_values)
    ideology_similarity = 1 / (1 + ideology_similarity)  # Normalize to [0, 1] range (closer is more similar)

    return ideology_similarity

    
def compute_agent_similarity(agents):
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

    # Compute TF-IDF cosine similarity for text data
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(text_data)
    text_similarity = cosine_similarity(tfidf_matrix)

    # Compute political ideology similarity
    ideology_similarity = compute_ideology_similarity(agents)

    # Combine similarities with a weighted average
    combined_similarity = 0.7 * traits_similarity + 0.3 * text_similarity + 0.2 * ideology_similarity

    return combined_similarity


def find_extreme_agents(similarity_matrix, agents):
    num_agents = len(agents)
    max_similarity = -1
    min_similarity = float('inf')
    most_similar_pair = ()
    most_different_pair = ()

    for i in range(num_agents):
        for j in range(i+1 , num_agents):  # Only consider unique pairs
            similarity = similarity_matrix[i, j]
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_pair = (i, j)
            if similarity < min_similarity:
                min_similarity = similarity
                most_different_pair = (i, j)
    
    return most_similar_pair, most_different_pair
