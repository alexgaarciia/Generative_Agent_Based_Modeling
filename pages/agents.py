import streamlit as st


# Page personalization
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")
st.title("Agent Personalization Page")


# Agent creation form
with st.form(key="agent_creation_option"):
    selected_pair = st.radio("Please choose your preferred method for agent creation:",
        options=[
            "Load pre-existing agents from a JSON file",
            "Manually create new agents"])

    submitted = st.form_submit_button("Proceed", use_container_width=True)

    if submitted:
        if "Load pre-existing agents from a JSON file" in selected_pair:
            page_file = "./pages/agents_json.py"
            st.switch_page(page_file)
        else:
            page_file = "./pages/agents_manual.py"
            st.switch_page(page_file)
            

# "Go Back" Button
st.markdown("<br>", unsafe_allow_html=True)
_, _ , _, col1, _, _, _ = st.columns([1, 1, 1, 1, 1, 1, 1])  
with col1:
    home_button = st.button("Go Back", use_container_width=True)
    if home_button:
        # Switch to the selected page
        page_file = "./pages/dashboard.py"
        st.switch_page(page_file)
