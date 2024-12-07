import streamlit as st

# Dictionary mapping page names to functions
pages = {
    "Details": "./pages/details.py",
    "Agents Creation": "./pages/agents_creation.py",
    "Experiment": "./pages/experiment.py",
    "Agent Confrontation": "./pages/agents_confrontation.py"
}

# Key Features Section
st.markdown("### Simulation Configuration")
api_key = st.text_input("Enter your API Key", type="password", help="Your API key is required for running simulations.")

# Model selection
model_options = ["Select a Model", "Local LM1", "Local LM2", "Local LM3"]
selected_model = st.selectbox("Select a Model for Simulation", model_options, help="Choose a model to use for simulations.")


if api_key and selected_model != "Select a Model":
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Select a Simulation Option")

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
else:
    st.warning("Please enter your API key and select a model to proceed.")

# Buttons
st.markdown("<br>", unsafe_allow_html=True)

_, _ , _, col1, _, _, _ = st.columns([1, 1, 1, 1, 1, 1, 1])  
with col1:
    home_button = st.button("Go Back", use_container_width=True)
    if home_button:
        # Switch to the selected page
        page_file = pages["Details"]
        st.switch_page(page_file)
        