import streamlit as st
from simulations.model_validation import validate_model

st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

# Initialize session state variables
if "api_key" not in st.session_state:
    st.session_state["api_key"] = None

if "selected_model" not in st.session_state:
    st.session_state["selected_model"] = None

# Dictionary mapping page names to functions
pages = {
    "Details": "./pages/details.py",
    "Agents Creation": "./pages/agents_creation.py",
    "Experiment": "./pages/experiment.py",
    "Agent Confrontation": "./pages/agents_confrontation.py",
}

# Simulation Configuration
st.markdown("### Simulation Configuration")
with st.form("simulation_form"):
    # API Key Input
    api_key = st.text_input("Enter your API Key", type="password", help="Your API key is required for running simulations.")
    # Model Selection
    model_options = ["Select a Model", "Qwen/Qwen2.5-Coder-3B-Instruct-GGUF", "Local LM2", "Local LM3"]
    selected_model = st.selectbox("Select a Model for Simulation", model_options, help="Choose a model to use for simulations.")
    # Submit Button
    submitted = st.form_submit_button("Submit")

    if submitted:
        if api_key:
            st.session_state["api_key"] = api_key
        if selected_model != "Select a Model":
            st.session_state["selected_model"] = selected_model

if st.session_state["api_key"] and st.session_state["selected_model"]:
    st.info("Validating connection with the LLM...")
    # Validate the model connection
    validation_success = validate_model(st.session_state["api_key"], st.session_state["selected_model"])

    if validation_success:
        st.success("The model is connected and validated successfully.")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Select a Simulation Option")
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
        st.error("Model validation failed. Please check the API key and model name.")
        st.stop()
else:
    st.warning("Please enter your API key and select a model to proceed.")

# Go Back Button
st.markdown("<br>", unsafe_allow_html=True)
_, _ , _, col1, _, _, _ = st.columns([1, 1, 1, 1, 1, 1, 1])  
with col1:
    home_button = st.button("Go Back", use_container_width=True)
    if home_button:
        # Switch to the selected page
        page_file = pages["Details"]
        st.switch_page(page_file)
