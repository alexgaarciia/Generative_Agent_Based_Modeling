# to run locally:  streamlit run C:\path here \main.py
import streamlit as st

# Dictionary mapping page names to functions
pages = {
    "Home": "./pages/main.py",
    "About": "./pages/about.py",
    "Key Features": "./pages/features.py"
    # "Agent Creation": agent_creation,
    # "Agent Comparison": agent_comparison,
}

# Main page title
st.markdown("<h1 style='text-align: center;'>🤖Designing Reliable Experiments with Generative Agent-Based Models🤖</h1>",
            unsafe_allow_html=True)

# Button to switch page
about_button = st.button("About")
feature_button = st.button("Key Features")
if about_button:
    # Switch to the selected page
    page_file = pages["About"]
    st.switch_page(page_file)

if feature_button:
    # Switch to the selected page
    page_file = pages["Key Features"]
    st.switch_page(page_file)
