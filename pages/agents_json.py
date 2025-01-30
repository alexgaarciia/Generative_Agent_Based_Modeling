import json
import streamlit as st
from simulations.agent_creation import validate_agents_file


# Page personalization
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")
st.title("Agent Personalization Page")

st.write("To load pre-existing agents, please upload the JSON file containing the agent data. "
         "Ensure that the file is structured correctly for seamless integration.")
            
uploaded_file = st.file_uploader(
    "Choose a JSON file with agent data",
    type="json", 
    label_visibility="collapsed"
)

if uploaded_file is not None:
    try:
        # Read the content of the uploaded file
        file_content = uploaded_file.read().decode("utf-8")
        agents_data = json.loads(file_content)  # Convert string content into JSON object (list of agents)

        # Validate the structure of the agents
        is_valid, message = validate_agents_file(agents_data)
        
        if is_valid:
            # Store agents data in session state
            st.session_state["agents"] = agents_data
            st.success("Agents loaded successfully!")
        else:
            st.error(message)

    except json.JSONDecodeError:
        st.error("The uploaded file is not a valid JSON.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


# "Go Back" and "Go to Dashboard" buttons
st.markdown("<br>", unsafe_allow_html=True)
_ , col1, col2, _ = st.columns([1, 1, 1, 1])  
with col1:
    go_back = st.button("Go Back", use_container_width=True)
    if go_back:
        # Switch to the selected page
        page_file = "./pages/agents.py"
        st.switch_page(page_file)

with col2:
    dashboard_button = st.button("Go to Dashboard", use_container_width=True)
    if dashboard_button:
        # Switch to the selected page
        page_file = "./pages/dashboard.py"
        st.switch_page(page_file)
        