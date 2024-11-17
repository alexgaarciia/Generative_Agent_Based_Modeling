import streamlit as st

# Load the CSS file and apply the styles
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Dictionary mapping page names to functions
pages = {
    "Start": "./pages/start.py",
}

# Header
st.markdown("""<h1>Ready to explore Generative Agent-Based Modeling?</h1>""", unsafe_allow_html=True)

# Button
start_button = st.button("Let's Go!")
if start_button:
    # Switch to the "Start" page
    page_file = pages["Start"]
    st.switch_page(page_file)
