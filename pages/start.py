import streamlit as st

# Dictionary mapping page names to functions
pages = {
    "Home": "main.py",
    "Details": "./pages/details.py",
    "Key Features": "./pages/features.py",
    "About Us": "./pages/about_us.py"
}

# Create n columns to place the buttons side by side
col1, col2, col3 = st.columns(3)

with col1:
    details_button = st.button("Details")
    if details_button:
        # Switch to the "About" page
        page_file = pages["Details"]
        st.switch_page(page_file)

with col2:
    feature_button = st.button("Key Features")
    if feature_button:
        # Switch to the "Key Features" page
        page_file = pages["Key Features"]
        st.switch_page(page_file)

with col3:
    about_us_button = st.button("About Us")
    if about_us_button:
        # Switch to the "About Us" page
        page_file = pages["About Us"]
        st.switch_page(page_file)
