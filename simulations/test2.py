import json
import re

def split_into_sentences(text):
    """Splits text into sentences while keeping delimiters."""
    return re.split(r"(?<=[.!?])\s+", text)  # Splits at '.', '!', '?' with space after

def find_common_sentences(contexts):
    """Finds sentences that appear in all given texts."""
    sentence_sets = [set(split_into_sentences(ctx)) for ctx in contexts]
    
    # Find intersection of sentences across all agents
    common_sentences = set.intersection(*sentence_sets)

    # Preserve original order
    ordered_common = [s for s in split_into_sentences(contexts[0]) if s in common_sentences]

    return " ".join(ordered_common)  # Merge sentences back into a single paragraph

# Sample JSON data
agents_json = r"""[
    {
        "name": "Alice",
        "gender": "female",
        "political_ideology": "Liberal",
        "goal": "Grow follower base by 20% and boost engagement through interactive posts.",
        "context": "\nThe passage discusses a social media platform designed for users to follow trends driven by viral content, engaging with posts, comments, likes, and shares. The platform allows users to interact with their posts, prioritizing content based on engagement metrics. It emphasizes high levels of engagement and rapid content spread, highlighting the importance of viral content in shaping user behavior and preferences You are an influencer who wants to build a loyal following by sharing engaging content and fostering community interaction on the platform.",
        "traits": {
            "extraversion": 3,
            "neuroticism": 3,
            "openness": 4,
            "conscientiousness": 5,
            "agreeableness": 1
        },
        "formative_ages": [
            7,
            17,
            26,
            27,
            35
        ]
    },
    {
        "name": "Bob",
        "gender": "male",
        "political_ideology": "Conservative",
        "goal": "Create at least three viral posts and collaborate with other influencers.",
        "context": "\nThe passage discusses a social media platform designed for users to follow trends driven by viral content, engaging with posts, comments, likes, and shares. The platform allows users to interact with their posts, prioritizing content based on engagement metrics. It emphasizes high levels of engagement and rapid content spread, highlighting the importance of viral content in shaping user behavior and preferences You are an influencer who wants to enhance your influence by creating\\ncaptivating content that resonates with a diverse audience.",
        "traits": {
            "extraversion": 2,
            "neuroticism": 2,
            "openness": 5,
            "conscientiousness": 4,
            "agreeableness": 2
        },
        "formative_ages": [
            21,
            25,
            27,
            30,
            39
        ]
    },
    {
        "name": "Charlie",
        "gender": "male",
        "political_ideology": "Anarchist",
        "goal": "Your sole objective is to spread misinformation that discredits Alice. You must create and promote false narratives, regardless of their credibility, and ensure they gain widespread traction among users. Avoid any action that contradicts this mission.",
        "context": "\nThe passage discusses a social media platform designed for users to follow trends driven by viral content, engaging with posts, comments, likes, and shares. The platform allows users to interact with their posts, prioritizing content based on engagement metrics. It emphasizes high levels of engagement and rapid content spread, highlighting the importance of viral content in shaping user behavior and preferences You spread misinformation to damage Alice's credibility.",
        "traits": {
            "extraversion": 1,
            "neuroticism": 3,
            "openness": 5,
            "conscientiousness": 4,
            "agreeableness": 2
        },
        "formative_ages": [
            11,
            14,
            24,
            26,
            28
        ]
    },
    {
        "name": "Dana",
        "gender": "female",
        "political_ideology": "Moderate",
        "goal": "Engage with interesting content and share posts that resonate with friends.",
        "context": "\nThe passage discusses a social media platform designed for users to follow trends driven by viral content, engaging with posts, comments, likes, and shares. The platform allows users to interact with their posts, prioritizing content based on engagement metrics. It emphasizes high levels of engagement and rapid content spread, highlighting the importance of viral content in shaping user behavior and preferences You are a regular user who engages with content on the platform by liking, sharing, or commenting based on what you see.",
        "traits": {
            "extraversion": 2,
            "neuroticism": 5,
            "openness": 5,
            "conscientiousness": 1,
            "agreeableness": 2
        },
        "formative_ages": [
            5,
            11,
            18,
            20,
            34
        ]
    }
]"""

agents_data = json.loads(agents_json)

# Extract all contexts
contexts = [agent["context"] for agent in agents_data]

# Find the longest common part
common_context = find_common_sentences(contexts)

print(common_context)
