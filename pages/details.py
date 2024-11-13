import streamlit as st

pages = {
    "Home": "main.py",
}

st.markdown("<h3>About This Platform: A Hands-On Tool for GABM Experimentation</h3>", unsafe_allow_html=True)
st.write(
    """
    This platform is designed to help researchers and users with minimal programming experience create and experiment with
    generative agent-based models (GABMs). Leveraging the Concordia framework, this tool makes it easy to build custom agents,
    explore their attributes, and conduct reliable experiments, all through an accessible and user-friendly interface.
    """
)

# Buttons
home_button = st.button("Home")
if home_button:
    # Switch to the selected page
    page_file = pages["Home"]
    st.switch_page(page_file)
