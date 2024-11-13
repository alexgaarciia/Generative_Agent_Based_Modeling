import streamlit as st

# Dictionary mapping page names to functions
pages = {
    "Home": "main.py",
    "About": "./pages/about.py",
    "Key Features": "./pages/features.py"
    #"Agent Creation": agent_creation,
    #"Agent Comparison": agent_comparison,
}

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

# Buttons
home_button = st.button("Home")
if home_button:
    # Switch to the selected page
    page_file = pages["Home"]
    st.switch_page(page_file)

