import streamlit as st
from simulations.model_validation import validate_model


# Dictionary mapping page names to functions
pages = {
    "Details": "./pages/details.py",
    "Agents Creation": "./pages/agents.py",
    "Experiment": "./pages/experiment.py",
    "confrontation1": "./pages/confrontation_personalized.py",
    "confrontation2": "./pages/confrontation_similar.py"
}


# Page personalization
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")


# Initialize session state variables
if "api_key" not in st.session_state:
    st.session_state["api_key"] = None
if "selected_model" not in st.session_state:
    st.session_state["selected_model"] = None
if "model_validated" not in st.session_state:
    st.session_state["model_validated"] = False


# Simulation Configuration
st.markdown("### LLM Configuration")
with st.form("simulation_form"):
    # API Key Input
    api_key = st.text_input("Enter your API Key", type="password", help="Your API key is required for running simulations.")

    # Model Selection
    model_options = ["Select a Model", "gpt-4", "gpt-3.5-turbo", "codestral-latest"]
    selected_model = st.selectbox("Select a Model for Simulation", model_options, help="Choose a model to use for simulations.")

    # Buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        home_button = st.form_submit_button("Go Back", use_container_width=True)
        if home_button:
            page_file = pages["Details"]
            st.switch_page(page_file)
    with col2:  
        validate_button = st.form_submit_button("Submit", use_container_width=True)
        if validate_button:
            if api_key:
                st.session_state["api_key"] = api_key
            if selected_model != "Select a Model":
                st.session_state["selected_model"] = selected_model
    with col3: 
        reset_button = st.form_submit_button("Reset", use_container_width=True)
        if reset_button:
            st.session_state["api_key"] = None
            st.session_state["selected_model"] = None
            st.session_state["model_validated"] = False


# Validation check only if the model has not been validated
# st.session_state["model_validated"] = True 
if st.session_state["api_key"] and st.session_state["selected_model"]:
    if not st.session_state["model_validated"]:
        with st.spinner("Validating connection with the LLM..."):
            validation_success = validate_model(st.session_state["api_key"], st.session_state["selected_model"])
        if validation_success:
            st.session_state["model_validated"] = True
            st.success("The model is connected and validated successfully.")
        else:
            st.error("Model validation failed. Please check the API key and model name.")
            st.stop()
    else:
        st.success("Model already validated.")

    # After successful validation, show the simulation options
    if st.session_state["model_validated"]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Select a Simulation Option")

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        with col1:
            if  st.button("👤 Create Agents 👤", use_container_width=True):
                page_file = pages["Agents Creation"]
                st.switch_page(page_file)
        with col2:
            if st.button("⚗️ Run Experiments ⚗️", use_container_width=True):
                page_file = pages["Experiment"]
                st.switch_page(page_file)
        with col3:
            if st.button("🤼‍♂️ Confront Agents of My Choice 🤼‍♂️", use_container_width=True):
                page_file = pages["confrontation1"]
                st.switch_page(page_file)
        with col4:
            if st.button("🟰 Confront Similar/Different Agents 🟰", use_container_width=True):
                page_file = pages["confrontation2"]
                st.switch_page(page_file)
else:
    st.warning("Please enter your API key and select a model to proceed.")
