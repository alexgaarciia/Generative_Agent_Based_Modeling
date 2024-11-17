import streamlit as st

# Dictionary mapping page names to functions
pages = {
    "Home": "main.py",
    "Details": "./pages/details.py",
    "Key Features": "./pages/features.py",
    "About Us": "./pages/about_us.py"
}

st.markdown("<h3>About This Platform: A Hands-On Tool for GABM Experimentation</h3>", unsafe_allow_html=True)
st.write(
    """
    This platform is designed to help researchers and users with minimal programming experience create and experiment with
    generative agent-based models (GABMs). Leveraging the Concordia framework, this tool makes it easy to build custom agents,
    explore their attributes, and conduct reliable experiments, all through an accessible and user-friendly interface.
    """
)


# Create n columns to place the buttons side by side
col1, col2, col3, col4 = st.columns(4)

with col1:
    home_button = st.button("Home")
    if home_button:
        # Switch to the selected page
        page_file = pages["Home"]
        st.switch_page(page_file)

with col2:
    details_button = st.button("Details")
    if details_button:
        # Switch to the "About" page
        page_file = pages["Details"]
        st.switch_page(page_file)
    

with col3:
    feature_button = st.button("Key Features")
    if feature_button:
        # Switch to the "Key Features" page
        page_file = pages["Key Features"]
        st.switch_page(page_file)

with col4:
    about_us_button = st.button("About Us")
    if about_us_button:
        # Switch to the "About Us" page
        page_file = pages["About Us"]
        st.switch_page(page_file)