import streamlit as st

# Dictionary mapping page names to functions
pages = {
    "Details": "./pages/details.py",
    "Agents Creation": "./pages/agents_creation.py",
    "Experiment": "./pages/experiment.py",
    "Agent Confrontation": "./pages/agents_confrontation.py"
}

# Key Features Section
st.markdown("## Under Construction")

# Different options of the page
col1, col2, col3 = st.columns(3)
with col1:
    agents_creation_button = st.button("Create Agents")
    if agents_creation_button:
        page_file = pages["Agents Creation"]
        st.switch_page(page_file)

with col2:
    simulation_button = st.button("Run Experiments")
    if simulation_button:
        page_file = pages["Experiment"]
        st.switch_page(page_file)

with col3:
    confrontation_button = st.button("Agent Confrontation")
    if confrontation_button:
        page_file = pages["Agent Confrontation"]
        st.switch_page(page_file)

# Buttons
st.markdown("<br>", unsafe_allow_html=True)
home_button = st.button("Go Back")
if home_button:
    # Switch to the selected page
    page_file = pages["Details"]
    st.switch_page(page_file)
