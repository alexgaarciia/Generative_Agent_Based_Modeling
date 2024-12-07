import streamlit as st
from simulations.model_validation import validate_model

# Retrieve API key and model name from session state
GPT_API_KEY = st.session_state.get("api_key", "")
GPT_MODEL_NAME = st.session_state.get("selected_model", "")

# Validate the model connection
validation_success = validate_model(GPT_API_KEY, GPT_MODEL_NAME)

if validation_success:
    st.success("The model is connected and validated successfully.")
else:
    st.error("Model validation failed. Please check the API key and model name.")
    st.stop()

# Proceed with the rest of the agents creation logic
st.markdown("### Agent Creation")
# Your agent creation logic here
