## 1️⃣ Introduction
This repository represents the practical part of my Final Degree Project, which seeks to democratize access to GABM and generative agents in two steps:
1. Documenting the accessibility challenges and opportunities of Generative Agent-Based Modeling (GABM) in a scientific context.
2. Developing an accessible, easy-to-use platform that allows a broader audience to design, simulate, and analyze generative agents without requiring advanced technical skills.

While the first objective is addressed through a dedicated scientific publication ([paper here](https://arxiv.org/abs/2411.07038)), this repository is focused on the second goal: providing an open-source, intuitive platform that gives anyone the chance for analyzing and understanding how generative agents make decisions and interact across various contexts, without the need for technical skills.

To accomplish this, a platform was developed using Streamlit, built on top of a library specialized in agent modeling, [Concordia](https://github.com/google-deepmind/concordia). It makes it easy to create and use models where agents act on their own. You can define environments with a special agent called the Game Master (GM), who manages the world where player agents interact. The agents say what they want to do in simple language, and the GM turns their words into actions.

The application contains different modules, allowing users to:
- Confront all defined agents, 
- Select and confront a specific subset of agents, 
- Identify and confront the most similar or most different agents

The comparisons between agents use machine learning techniques such as BERT-based embeddings and cosine similarity to group and differentiate them based on psychological traits, goals, context, and political ideology.

## 🔍 Platform Overview
- LLM Configuration: Set and verify your API key and choose the desired large language model for agent reasoning.
- Agent Creation: Design and customize agents using either a guided form or by uploading a JSON.
- Simulation Options: Choose from the three options of simulations, all powered by the Concordia library.
- Experiment Configuration: Easily set up and modify simulation parameters and scenarios.
- Results Visualization: Monitor and analyze simulation outcomes.

## 📂 Repository Resources
To help navigate the repository, there are several .md files in the repository, explaining:
- [Project structure](https://github.com/alexgaarciia/Generative_Agent_Based_Modeling/blob/main/docs/REPOSITORY_STRUCTURE.md): Overview of how the repository is organized and what each folder/file does. 
- [How to run locally](https://github.com/alexgaarciia/Generative_Agent_Based_Modeling/blob/main/docs/RUN_LOCALLY.md): Step-by-step instructions to set up and run the platform locally.

## 📹 Explanatory YouTube Video
You can also take a look at this video, where I go through the functionalitites of the platform! [Click here](https://youtu.be/8t1rYQrq4Z4)
