# to run locally:  streamlit run C:\path here \main.py

import streamlit as st

# Main page title
st.markdown("<h1 style='text-align: center;'>🤖Designing Reliable Experiments with Generative Agent-Based Models🤖</h1>", unsafe_allow_html=True)
st.markdown("<br></br>", unsafe_allow_html=True)

# Platform Overview Section
st.markdown("<h3>About This Platform: A Hands-On Tool for GABM Experimentation</h3>", unsafe_allow_html=True)
st.write(
    """
    This platform is designed to help researchers and users with minimal programming experience create and experiment with
    generative agent-based models (GABMs). Leveraging the Concordia framework, this tool makes it easy to build custom agents,
    explore their attributes, and conduct reliable experiments, all through an accessible and user-friendly interface.
    """
)

# Key Features Section
st.markdown("## Key Features of the Generative Agent-Based Modeling Platform")
st.write(
    """
    - **Create Custom Agents**: Design virtual agents with unique attributes and characteristics.
    - **Customize Agents Easily**: Personalize agents to fit specific experimental needs or personality traits.
    - **Display Agent Information**: Access and review detailed information about each created agent.
    - **Compare Personalities and Ideologies**: Contrast agents with similar or differing political and ideological profiles.
    """
)

# Sidebar menu for navigation (para más adelante)
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Home", "Agent Creation", "Agent Comparison"])