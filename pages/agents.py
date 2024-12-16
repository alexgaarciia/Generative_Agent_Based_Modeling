import streamlit as st
from simulations.agents_creation import make_random_formative_ages

# Streamlit app
st.title("Agent Personalization Page")

# Step 1: Input shared context
st.subheader("Step 1: Define Shared Context")
shared_context = st.text_area(
    "Provide the shared context for all agents:"
)

# Step 2: Select number of agents
st.subheader("Step 2: Select Number of Agents")
num_agents = st.slider(
    "Select the number of agents (4 to 6):", min_value=4, max_value=6, value=4
)

# Initialize agent list and current step
if 'agents' not in st.session_state:
    st.session_state.agents = []
if 'current_agent' not in st.session_state:
    st.session_state.current_agent = 0
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Function to create agent step by step
def create_agent():
    agent_index = st.session_state.current_agent
    st.write(f"**Agent {agent_index + 1}**")

    with st.form(key=f"agent_form_{agent_index}"):
        name = st.text_input(f"Name of Agent {agent_index + 1}:")
        gender = st.selectbox(f"Gender of Agent {agent_index + 1}:", options=["male", "female"])
        goal = st.text_area(f"Goal of Agent {agent_index + 1}:")
        context = st.text_area(f"Context for Agent {agent_index + 1}:", value=shared_context,)
        
        st.subheader(f"Big Five Personality Traits for Agent {agent_index + 1}:")
        extraversion = st.selectbox("Extraversion", [1, 2, 3, 4, 5])
        neuroticism = st.selectbox("Neuroticism", [1, 2, 3, 4, 5])
        openness = st.selectbox("Openness", [1, 2, 3, 4, 5])
        conscientiousness = st.selectbox("Conscientiousness", [1, 2, 3, 4, 5])
        agreeableness = st.selectbox("Agreeableness", [1, 2, 3, 4, 5])

        # Formative Ages (random values)
        formative_ages = make_random_formative_ages

        # Submit button for the form
        submit_button = st.form_submit_button(label="Save Agent")

        # If the form is submitted, save the data and move to the next agent
        if submit_button:
            agent = {
                "name": name,
                "gender": gender,
                "goal": goal,
                "context": context,
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
    st.subheader("Step 4: Review and Save Agents")
    if st.button("Save Agents"):
        st.write("**Saved Agents:**")
        for agent in st.session_state.agents:
            st.json(agent)
        st.success("Agents saved successfully!")

else:
    st.subheader("Step 3: Create Agents")
    create_agent()
