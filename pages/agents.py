import json
import random
import streamlit as st
from simulations.simulation_runner import create_generic_knowledge


# Page personalization
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")
st.title("Agent Personalization Page")


# Initialize session state variables
if "generated_generic_knowledge" not in st.session_state:
    st.session_state["generated_generic_knowledge"] = False


# Step 1: Input shared context
st.markdown("### Step 1: Define Shared Context")
st.markdown(
    """
    In this section, you need to provide a shared context for the simulation participants. 
    This context will be the memory shared by all players and the Game Master. 
    It's essential to describe the background or scenario that connects all the agents in your simulation.
    """
)
with st.form("shared_context_form"):
    shared_context = st.text_area(
        "Please write the shared context here:",
        help="This context will serve as a common background for all participants in the simulation.",
    )
    submit_button = st.form_submit_button("Submit")

    if submit_button:
        if not shared_context.strip():
            st.warning("The shared context cannot be empty. Please provide a description.")
        else:
            if not st.session_state["generated_generic_knowledge"]:
                with st.spinner("Summarizing the shared context..."):
                    st.session_state["shared_context"] = shared_context
                    generic_knowledge = create_generic_knowledge(shared_context)

                    if generic_knowledge:
                        st.session_state["generated_generic_knowledge"] = True
                        st.session_state["generic_knowledge"] = generic_knowledge
                        st.success("Shared context submitted successfully!")


# Only display the next steps after the generic knowledge is generated
if st.session_state["generated_generic_knowledge"]:
    # Step 2: Select number of agents
    st.markdown("### Step 2: Select Number of Agents")
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
    def make_random_formative_ages():
        return sorted(random.sample(range(5, 40), 5))

    def create_agent():
        agent_index = st.session_state.current_agent
        st.write(f"**Agent {agent_index + 1}**")

        with st.form(key=f"agent_form_{agent_index}"):
            name = st.text_input(f"Name of Agent {agent_index + 1}:")
            gender = st.selectbox(f"Gender of Agent {agent_index + 1}:", options=["male", "female"])
            goal = st.text_area(f"Goal of Agent {agent_index + 1}:")
            temp_context = st.text_area(f"Context for Agent {agent_index + 1}:")
            context = st.session_state["generic_knowledge"] + " " + temp_context
            
            st.subheader(f"Big Five Personality Traits for Agent {agent_index + 1}:")
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
        st.markdown("### Step 4: Review and Save Agents")
        _, _ , _, col1, _, _, _ = st.columns([1, 1, 1, 1, 1, 1, 1])  
        with col1:
            if st.button("Save Agents"):
                # Save agents to a JSON file
                with open("agents.json", "w") as f:
                    json.dump(st.session_state.agents, f, indent=4)
                
        if st.session_state.agents:
            st.success("Agents saved successfully!")
            st.write("**Saved Agents:**")
            for agent in st.session_state.agents:
                st.json(agent)
    else:
        st.markdown("### Step 3: Create Agents")
        create_agent()


# "Go Back" Button
st.markdown("<br>", unsafe_allow_html=True)
_, _ , _, col1, _, _, _ = st.columns([1, 1, 1, 1, 1, 1, 1])  
with col1:
    home_button = st.button("Go Back", use_container_width=True)
    if home_button:
        # Switch to the selected page
        page_file = "./pages/dashboard.py"
        st.switch_page(page_file)
