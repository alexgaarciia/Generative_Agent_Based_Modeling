import streamlit as st

st.set_page_config(layout="centered", initial_sidebar_state="collapsed")


# Dictionary mapping page names to functions
pages = {
    "Confrontation Main Page": "./pages/confrontation.py",
}


# Key Features Section
st.markdown("## Under Construction")


# Buttons
st.markdown("<br>", unsafe_allow_html=True)
_, _ , _, col1, _, _, _ = st.columns([1, 1, 1, 1, 1, 1, 1])  
with col1:
    home_button = st.button("Go Back", use_container_width=True)
    if home_button:
        # Switch to the selected page
        page_file = pages["Confrontation Main Page"]
        st.switch_page(page_file)
