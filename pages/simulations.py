import streamlit as st

# Dictionary mapping page names to functions
pages = {
    "Details": "./pages/details.py",
}

# Key Features Section
st.markdown("## Under Construction")

# Buttons
home_button = st.button("Go Back")
if home_button:
    # Switch to the selected page
    page_file = pages["Details"]
    st.switch_page(page_file)
