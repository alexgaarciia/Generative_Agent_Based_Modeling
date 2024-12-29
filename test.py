import json
from simulations.agent_similarity import *


# Read agents from agents.json
with open('agents.json', 'r') as f:
    agents = json.load(f)

# Compute similarity matrix
similarity_matrix = compute_agent_similarity(agents)

# Find the most similar and most different agent pairs
most_similar, most_different = find_extreme_agents(similarity_matrix, agents)

# Output results
agent_names = [agent["name"] for agent in agents]

print(similarity_matrix)
print(f"The two most similar agents are: {agent_names[most_similar[0]]} and {agent_names[most_similar[1]]}")
print(f"The two most different agents are: {agent_names[most_different[0]]} and {agent_names[most_different[1]]}")
