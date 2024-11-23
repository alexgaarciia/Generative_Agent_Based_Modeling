import streamlit as st

# Dictionary mapping page names to functions
pages = {
    "Home": "main.py",
}

# Key Features Section
st.markdown("## Under Construction")

# Buttons
home_button = st.button("Home")
if home_button:
    # Switch to the selected page
    page_file = pages["Home"]
    st.switch_page(page_file)
