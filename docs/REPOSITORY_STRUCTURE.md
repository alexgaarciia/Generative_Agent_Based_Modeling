# Repository Structure

This document describes the structure of the repository for the final project. You can find the purpose of each folder and key files.
```
📁 Generative_Agent_Based_Modeling
├── 📂 .streamlit -> Streamlit configuration files
│   └── 📄 config.toml -> App-level settings and customizations
├── 📂 docs -> Platform documentation and usage instructions
│   ├── 📄 REPOSITORY_STRUCTURE.md -> Description of the repository layout
│   └── 📄 RUN_LOCALLY.md -> Guide to run the platform locally
├── 📂 images -> Custom figures created for the thesis
│   ├── 📄 relu.png, sigmoid.png, softmax.png, tanh.png -> Activation function plots
│   └── 📄 figures_activation_functions.ipynb -> Notebook for generating the images
├── 📂 pages -> Streamlit frontend pages of the platform
│   ├── 📄 about_us.py -> About page
│   ├── 📄 agents.py -> Interface for creating or uploading agents via form or JSON
│   ├── 📄 confrontation_personalized.py -> Page to carry out a personalized simulation between two user-selected agents
│   ├── 📄 confrontation_similar.py -> Simulation page to confront the most similar or most different agents
│   ├── 📄 dashboard.py -> Central dashboard page
│   ├── 📄 details.py -> Page that introduces GABM, explains platform features, and links to main sections
│   └── 📄 experiment.py -> Simulation page to involve all defined agents
├── 📂 simulations -> Backend logic and simulation engine
│   ├── 📂 concordia -> Concordia library
│   ├── 📄 agent_creation.py -> Agent creation and validation functions
│   ├── 📄 agent_similarity.py -> Utility functions for computing similarity between agents
│   ├── 📄 model_validation.py -> Logic for LLM connection validation
│   └── 📄 simulation_runner.py -> Core simulation execution logic
├── 📄 main.py -> Entry point for launching the Streamlit app
├── 📄 README.md -> Project overview and general instructions
├── 📄 requirements.txt -> Python dependencies for running the platform
└── 📄 style.css -> Custom styles for the UI
```
