import streamlit as st


# Page personalization
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")


# Initialize session state variables
if "agents" not in st.session_state:
    st.session_state["agents"] = []
if "agents_validated" not in st.session_state:
    st.session_state["agents_validated"] = False


# Dictionary mapping page names to functions
pages = {
    "Simulations": "./pages/simulations.py",
    "Agents": "./pages/agents.py",
    "confrontation1": "./pages/confrontation_personalized.py",
    "confrontation2": "./pages/confrontation_similar.py",
    "confrontation3": "./pages/confrontation_different.py",
}


# Verify agents
st.markdown("## Agent Arena")
if not st.session_state["agents_validated"]:
    with st.spinner("Verifying the existence of agents..."):
        if st.session_state["agents"]:
            st.session_state["agents_validated"] = True
            st.success("Agents found")
        else:
            st.error("The agents do not exist, please create them")
            _, _ , _, col1, _, _, _ = st.columns([1, 1, 1, 1, 1, 1, 1])  
            with col1:
                if st.button("Create Agents", use_container_width=True):
                    page_file = pages["Agents"]
                    st.switch_page(page_file)
                    st.stop()
else:
    # Show 3 possible options of agent confrontation in case of agent existance
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Confront Agents of My Choice", use_container_width=True):
            page_file = pages["confrontation1"]
            st.switch_page(page_file)
    with col2:
        if st.button("Confront Similar Agents", use_container_width=True):
            page_file = pages["confrontation2"]
            st.switch_page(page_file)
    with col3:
        if st.button("Confront Different Agents", use_container_width=True):
            page_file = pages["confrontation3"]
            st.switch_page(page_file)


# "Go Back" Button
st.markdown("<br>", unsafe_allow_html=True)
_, _ , _, col1, _, _, _ = st.columns([1, 1, 1, 1, 1, 1, 1])  
with col1:
    home_button = st.button("Go Back", use_container_width=True)
    if home_button:
        # Switch to the selected page
        page_file = pages["Simulations"]
        st.switch_page(page_file)
