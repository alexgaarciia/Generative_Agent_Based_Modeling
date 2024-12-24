import streamlit as st


# Dictionary mapping page names to functions
pages = {
    "Details": "./pages/details.py",
}


# Page Personalization
st.set_page_config(page_title="main", layout="wide", initial_sidebar_state="collapsed")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("""<h1>Ready to explore Generative Agent-Based Modeling?</h1>""", unsafe_allow_html=True)


# Button
details_button = st.button("Let's Go!")
if details_button:
    # Switch to the "Details" page
    page_file = pages["Details"]
    st.switch_page(page_file)
