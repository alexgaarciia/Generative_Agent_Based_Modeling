import streamlit as st

pages = {
    "Home": "main.py",
}

st.markdown("<h3>The Team</h3>", unsafe_allow_html=True)
st.write(
    """
    Team Details Here!
    """
)

# Buttons
home_button = st.button("Home")
if home_button:
    # Switch to the selected page
    page_file = pages["Home"]
    st.switch_page(page_file)
