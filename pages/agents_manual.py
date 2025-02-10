import json
import random
import datetime
import streamlit as st


# Page personalization
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")
st.title("Agent Personalization Page")


# Step 1: Select number of agents
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

# Function to create agent step by step
def make_random_formative_ages():
    return sorted(random.sample(range(5, 40), 5))

def create_agent():
    agent_index = st.session_state.current_agent

    with st.form(key=f"agent_form_{agent_index}"):
        st.markdown(f"## **Agent {agent_index + 1}**")
        name = st.text_input(f"Name of Agent {agent_index + 1}:")
        gender = st.selectbox(f"Gender of Agent {agent_index + 1}:", options=["Male", "Female"])
        political_ideology = st.selectbox(f"Political Ideology of Agent {agent_index + 1}:",
                                              options=["Liberal", "Conservative", "Moderate", "Libertarian", "Socialist", "Anarchist"])
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"#### Big Five Personality Traits for Agent {agent_index + 1}:")
        extraversion = st.selectbox("Extraversion", [1, 2, 3, 4, 5])
        neuroticism = st.selectbox("Neuroticism", [1, 2, 3, 4, 5])
        openness = st.selectbox("Openness", [1, 2, 3, 4, 5])
        conscientiousness = st.selectbox("Conscientiousness", [1, 2, 3, 4, 5])
        agreeableness = st.selectbox("Agreeableness", [1, 2, 3, 4, 5])

        # Formative Ages (random values)
        formative_ages = make_random_formative_ages()

        # Submit button for the form
        submit_button = st.form_submit_button(label="Save Agent")

        # If the form is submitted, save the data and move to the next agent
        if submit_button:
            agent = {
                "name": name,
                "gender": gender,
                "political_ideology": political_ideology,
                "traits": {
                    'extraversion': extraversion,
                    'neuroticism': neuroticism,
                    'openness': openness,
                    'conscientiousness': conscientiousness,
                    'agreeableness': agreeableness,
                },
                "formative_ages": formative_ages,
            }
            st.session_state.agents.append(agent)

            # Move to the next agent after submission
            if agent_index < num_agents - 1:
                st.session_state.current_agent += 1
                st.warning("Verify agent's details")
            else:
                st.session_state.form_submitted = True

# Display and save agents after all are created
if st.session_state.form_submitted:
    st.markdown("### Step 3: Review and Save Agents")
    _, _, _, col1, _, _, _ = st.columns([1, 1, 1, 1, 1, 1, 1])  
    with col1:
        if st.button("Save Agents"):
            # Generate a unique filename using the current timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"agents_{timestamp}.json"
            
            # Save agents to a JSON file
            with open(filename, "w") as f:
                json.dump(st.session_state.agents, f, indent=4)
                
    if st.session_state.agents:
        st.success("Agents saved successfully!")
        st.write("**Saved Agents:**")
        for agent in st.session_state.agents:
            st.json(agent)
else:
    st.markdown("### Step 2: Create Agents")
    create_agent()


# "Go Back" and "Go to Dashboard" buttons
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])  
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

with col3:
    erase_agents = st.button("Create New Agents", use_container_width=True)
    if erase_agents:
        st.session_state.pop("agents", None)
        st.session_state.pop("form_submitted", None)
        st.session_state.pop("current_agent", None)
        st.rerun()
        