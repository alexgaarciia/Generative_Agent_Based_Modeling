import streamlit as st

st.set_page_config(layout="centered", initial_sidebar_state="collapsed")


# Dictionary mapping page names to functions
pages = {
    "Simulations": "./pages/simulations.py",
}


# Key Features Section
st.markdown("## Under Construction")


# Buttons
home_button = st.button("Go Back")
if home_button:
    page_file = pages["Simulations"]
    st.switch_page(page_file)
