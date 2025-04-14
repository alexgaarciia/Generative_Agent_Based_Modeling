import json
import datetime
import streamlit as st
from simulations.agent_creation import validate_agents_file, create_agent


# Page personalization
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")
st.title("Agent Personalization Page")


# Initialize session state variables
if "creation_step" not in st.session_state:
    st.session_state["creation_step"] = 1 
if "agents" not in st.session_state:
    st.session_state["agents"] = []
if "current_agent" not in st.session_state:
    st.session_state["current_agent"] = 0
if "form_submitted" not in st.session_state:
    st.session_state["form_submitted"] = False


# Agent creation form
if st.session_state["creation_step"] == 1:    
    with st.form(key="agent_creation_option"):
        selected_pair = st.radio("Please choose your preferred method for agent creation:",
            options=[
                "Load pre-existing agents from a JSON file",
                "Manually create new agents"])

        col1, col2 = st.columns([1, 1])
        with col1:
            home_button = st.form_submit_button("Go to Dashboard", use_container_width=True)            
        with col2:
            next_pressed = st.form_submit_button("Next", use_container_width=True)
            
        if home_button:
            page_file = "./pages/dashboard.py"
            st.switch_page(page_file) 
        elif next_pressed:
            if "Load pre-existing agents from a JSON file" in selected_pair:
                st.session_state["creation_step"] = 2
                st.rerun()
            else:
                st.session_state["creation_step"] = 3
                st.rerun()

elif st.session_state["creation_step"] == 2:
    st.write("To load pre-existing agents, please upload the JSON file containing the agent data. "
            "Ensure that the file is structured correctly for seamless integration.")    
    
    example_json = [
        {
            "name": "Alice",
            "gender": "Female",
            "political_ideology": "Moderate",
            "traits": {
                "extraversion": 1,
                "neuroticism": 5,
                "openness": 5,
                "conscientiousness": 2,
                "agreeableness": 3
            },
            "formative_ages": [10, 15, 20, 30, 40]
        }
    ]
    with st.expander("See example format"):
        st.markdown("""
        **Each agent must follow this structure:**

        - **`name`**: A string with the agent’s name (e.g., Alice).
        - **`gender`**: Must be either Male or Female.
        - **`political_ideology`**: One of the following options: Liberal, Conservative, Moderate, Libertarian, Socialist, Anarchist.
        - **`traits`**: A dictionary with the agent’s psychological traits. Each trait is a number from **1 (low)** to **5 (high)**: extraversion, neuroticism, openness, conscientiousness, agreeableness.
        - **`formative_ages`**: A list of **5 ages** (integers) that were significant in the agent’s development.

        **Example JSON:**
        """)
        st.code(json.dumps(example_json, indent=4), language="json")

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
            
    col1, col2, col3 = st.columns([1, 1, 1])  
    with col1:
        go_back = st.button("Go Back", use_container_width=True)
        if go_back:
            st.session_state["creation_step"] = 1
            st.rerun()
    with col2:
        dashboard_button = st.button("Go to Dashboard", use_container_width=True)
        if dashboard_button:
            st.session_state["creation_step"] = 1
            page_file = "./pages/dashboard.py"
            st.switch_page(page_file)
    with col3:
        erase_agents = st.button("Create New Agents", use_container_width=True)
        if erase_agents:
            st.session_state.pop("agents", None)
            st.session_state["creation_step"] = 1
            st.rerun()   

elif st.session_state["creation_step"] == 3:
    st.markdown("### Step 1: Select Number of Agents")
    num_agents = st.slider(
        "Select the number of agents (4 to 6):", min_value=4, max_value=6, value=4)

    # Initialize agent list and current step
    if 'agents' not in st.session_state:
        st.session_state.agents = []
    if 'current_agent' not in st.session_state:
        st.session_state.current_agent = 0
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False

    # Display and save agents after all are created
    if st.session_state.form_submitted:
        st.markdown("### Step 3: Review and Save Agents")
        _, col1, _ = st.columns([1, 1, 1])  
        with col1:
            agents_json = json.dumps(st.session_state.agents, indent=4)
            st.download_button(
                label="Download Agents JSON",
                data=agents_json,
                file_name=f"agents_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
                    
        if st.session_state.agents:
            st.success("Agents saved successfully!")
            st.write("**Saved Agents:**")
            for agent in st.session_state.agents:
                st.json(agent)
    else:
        st.markdown("### Step 2: Create Agents")
        create_agent(num_agents)
   
    col1, col2, col3 = st.columns([1, 1, 1])  
    with col1:
        go_back = st.button("Go Back", use_container_width=True)
        if go_back:
            st.session_state["creation_step"] = 1
            st.rerun()
    with col2:
        dashboard_button = st.button("Go to Dashboard", use_container_width=True)
        if dashboard_button:
            st.session_state["creation_step"] = 1
            page_file = "./pages/dashboard.py"
            st.switch_page(page_file)
    with col3:
        erase_agents = st.button("Create New Agents", use_container_width=True)
        if erase_agents:
            st.session_state.pop("agents", None)
            st.session_state.pop("form_submitted", None)
            st.session_state.pop("current_agent", None)
            st.session_state["creation_step"] = 1
            st.rerun()         
                