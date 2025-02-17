import copy
import streamlit as st
from simulations.simulation_runner import * 
from simulations.agent_creation import create_generic_knowledge


# Page personalization
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")


# Initialize session state variables
if "agents" not in st.session_state:
    st.session_state["agents"] = []
if "memories" not in st.session_state:
    st.session_state["memories"] = []
if "agents_validated" not in st.session_state:
    st.session_state["agents_validated"] = False
if "players_built" not in st.session_state:
    st.session_state["players_built"] = False
if "players" not in st.session_state:
    st.session_state["players"] = []
if "gm_built" not in st.session_state:
    st.session_state["gm_built"] = False
if "gm" not in st.session_state:
    st.session_state["gm"] = None 
if "simulation_run" not in st.session_state:
    st.session_state["simulation_run"] = False
if "generated_generic_knowledge" not in st.session_state:
    st.session_state["generated_generic_knowledge"] = False
if "step" not in st.session_state:
    st.session_state["step"] = 1  
if "shared_context" not in st.session_state:
    st.session_state["shared_context"] = ""
if "agents_copied" not in st.session_state:
    st.session_state["agents_copied"] = copy.deepcopy(st.session_state["agents"])  # Copy only once


# Dictionary mapping page names to functions
pages = {
    "Dashboard": "./pages/dashboard.py",
    "Agents": "./pages/agents.py"
}


# Verify existence of agents
st.markdown("## Simulation Area")
if not st.session_state["agents_validated"]:
    with st.spinner("Verifying the existence of agents..."):
        if st.session_state["agents"]:
            st.session_state["agents_validated"] = True
        else:
            st.error("The agents do not exist, please create them")
            _, _, col1, _, _ = st.columns([1, 1, 1, 1, 1])  
            with col1:
                if st.button("Create Agents", use_container_width=True):
                    page_file = pages["Agents"]
                    st.switch_page(page_file)
                    
                    
# Step 1: Input shared context
if st.session_state["agents_validated"] and st.session_state["step"] == 1:
    st.markdown("### Step 1: Define Shared Context")
    st.write(
    """
    You need to provide a shared context for the simulation participants. This context will be the memory shared by all players and the Game Master. It's essential to describe the background or scenario that connects all the agents in your simulation.  

    For example, if we wanted to study agents' behavior in a social network, we might provide detailed descriptions of the platform’s features, how users interact with each other, and the mechanics that drive content engagement. This could include specifying how posts gain visibility, the role of algorithms in content promotion, and the potential impact of misinformation spread. By defining these details, we ensure that all participants share a clear understanding of the simulation environment.
    
    Next, define the interaction goal to specify the objective of the agent interactions within the simulation.
    """)

    with st.form(key="context_form"):
        # Input for shared context
        st.session_state["shared_context"] = st.text_area("Write the shared context here:")

        # Buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            # "Go to Dashboard" button
            home_button = st.form_submit_button("Go to Dashboard", use_container_width=True)            

        with col2:
            # "Next" button
            next_pressed = st.form_submit_button("Next", use_container_width=True)

    if next_pressed:
        if not st.session_state["shared_context"].strip():
            st.warning("The shared context cannot be empty. Please provide a description.")
        else:
            if not st.session_state["generated_generic_knowledge"]:
                with st.spinner("Summarizing the shared context..."):
                    generic_knowledge = create_generic_knowledge(st.session_state["shared_context"])

                    if generic_knowledge:
                        st.session_state["generated_generic_knowledge"] = True
                        st.session_state["generic_knowledge"] = generic_knowledge
                        for agent in st.session_state["agents_copied"]:
                            agent["context"] = generic_knowledge 
                        st.success("Shared context submitted successfully!")
            
            st.session_state["step"] = 2  # Move to Step 2
            st.rerun()  # Ensures the UI updates immediately
    if home_button:
        # Switch to the selected page
        page_file = pages["Dashboard"]
        st.switch_page(page_file)

# Step 2: Input goal and agent-specific context
elif st.session_state["step"] == 2:
    st.markdown("### Step 2: Define Agent Goal & Individual Context")  
    st.write(  
        "Specify the objective that will guide each agent's behavior within the simulation. "
        "Additionally, provide a unique context for each agent, defining their role and perspective within the experiment.")

    with st.form(key="goal_form"):
        agent_goals = {}
        agent_contexts = {}
        
        for agent in st.session_state["agents_copied"]:
            st.markdown(f"#### {agent['name']}")  # Display agent's name as a header
            agent_goals[agent["name"]] = st.text_area(f"Goal for {agent['name']}:", key=f"goal_{agent['name']}")
            agent_contexts[agent["name"]] = st.text_area(f"Context for {agent['name']}:", key=f"context_{agent['name']}")
                
                
        col1, col2 = st.columns([1, 1])
        with col1:
            back_pressed = st.form_submit_button("Back", use_container_width=True)
        with col2:
            submit_pressed = st.form_submit_button("Begin Simulation", use_container_width=True)

        if back_pressed:
            st.session_state["step"] = 1  # Go back to Step 1
            st.rerun()

        if submit_pressed:
            missing_fields = any(not goal.strip() or not context.strip() for goal, context in zip(agent_goals.values(), agent_contexts.values()))

            if missing_fields:
                st.warning("Each agent must have both a goal and a context.")
            else:
                for agent in st.session_state["agents_copied"]:
                    agent["goal"] = agent_goals[agent["name"]]
                    agent["context"] += agent_contexts[agent["name"]]
                    agent["ind_context"] = agent_contexts[agent["name"]]
                    
                st.session_state["step"] = 3  # Move to next step
                st.success("Agent goals and contexts have been successfully set!")
                st.rerun()

# Step 3: Being the simulation
elif st.session_state["step"] == 3:
    st.markdown("### Step 3: Run Simulation")
    
    # Create players and memories
    if st.session_state["agents_validated"] and st.session_state["generated_generic_knowledge"] and not st.session_state["players_built"]: 
        with st.spinner("Building players, this may take a while..."):        
            # Create players and memories
            player_configs = create_player_configs(st.session_state["agents_copied"])
            players, memories = build_players(player_configs)
            st.session_state["players"] = players
            st.session_state["memories"] = memories
            st.session_state["players_built"] = True
            st.success("Players built successfully")
    
    # Build the Game Master
    if st.session_state["players_built"] and not st.session_state["gm_built"]:
        with st.spinner("Building the Game Master..."):
            st.session_state["gm"] = build_gm(players=st.session_state["players"], 
                                            shared_context=st.session_state["generic_knowledge"])
            st.session_state["gm_built"] = True
            st.success("Game Master built successfully")

    # Run the simulation
    if st.session_state["gm_built"]:
        st.markdown("<br>", unsafe_allow_html=True)
        episode_length = st.number_input("Enter the number of episodes", min_value=4, value=4, max_value=12, step=1)
        if st.button("Run Episodes", use_container_width=True):
            with st.spinner(f"Running {episode_length} episodes..."):
                for _ in range(episode_length):
                    st.session_state["gm"].step()
                st.session_state["simulation_run"] = True
        
    # Button display
    _, col1, col2, _ = st.columns([1, 1, 1, 1])  
    with col1:
        home_button = st.button("Go to Dashboard", use_container_width=True)
        if home_button:
            # Switch to the selected page
            page_file = pages["Dashboard"]
            st.switch_page(page_file)
    with col2:
        new_simulation = st.button("New Simulation", use_container_width=True)
        if new_simulation:
            # Reset necessary session state variables
            st.session_state["step"] = 1  
            st.session_state["memories"] = []
            st.session_state["players_built"] = False
            st.session_state["gm_built"] = False
            st.session_state["gm"] = None
            st.session_state["simulation_run"] = False
            st.session_state["generated_generic_knowledge"] = False
            st.session_state["agents_validated"] = False
            st.session_state["shared_context"] = ""
            st.session_state["agents_copied"] = []
            st.rerun()
            
    # After the confrontation simulation, show the memory logs and summaries
    if st.session_state["simulation_run"]:
        st.markdown("<br>", unsafe_allow_html=True)
        summary(st.session_state["gm"], st.session_state["players"], st.session_state["memories"])
