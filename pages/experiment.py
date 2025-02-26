import copy
import streamlit as st
from simulations.simulation_runner import * 
from simulations.agent_creation import create_generic_knowledge

# Page personalization
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

# Initialize session state variables
if "agents" not in st.session_state:
    st.session_state["agents"] = []
if "exp_memories" not in st.session_state:
    st.session_state["exp_memories"] = []
if "exp_agents_validated" not in st.session_state:
    st.session_state["exp_agents_validated"] = False
if "exp_players_built" not in st.session_state:
    st.session_state["exp_players_built"] = False
if "exp_players" not in st.session_state:
    st.session_state["exp_players"] = []
if "exp_gm_built" not in st.session_state:
    st.session_state["exp_gm_built"] = False
if "exp_gm" not in st.session_state:
    st.session_state["exp_gm"] = None 
if "exp_simulation_run" not in st.session_state:
    st.session_state["exp_simulation_run"] = False
if "exp_generated_generic_knowledge" not in st.session_state:
    st.session_state["exp_generated_generic_knowledge"] = False
if "exp_step" not in st.session_state:
    st.session_state["exp_step"] = 1  
if "exp_shared_context" not in st.session_state:
    st.session_state["exp_shared_context"] = ""

# Ensure "exp_agents_copied" is only created when "_agents" is not empty
if "exp_agents_copied" not in st.session_state or not st.session_state["exp_agents_copied"]:
    st.session_state["exp_agents_copied"] = copy.deepcopy(st.session_state["agents"])

# Dictionary mapping page names to functions
pages = {
    "Dashboard": "./pages/dashboard.py",
    "Agents": "./pages/agents.py"
}

# Verify existence of agents
st.markdown("## Simulation Area")
if not st.session_state["exp_agents_validated"]:
    with st.spinner("Verifying the existence of agents..."):
        if st.session_state["agents"]:
            st.session_state["exp_agents_validated"] = True
        else:
            st.error("The agents do not exist, please create them")
            _, col1, _ = st.columns([1, 1, 1])  
            with col1:
                if st.button("Create Agents", use_container_width=True):
                    page_file = pages["Agents"]
                    st.switch_page(page_file)
                    
# Step 1: Input shared context
if st.session_state["exp_agents_validated"] and st.session_state["exp_step"] == 1:
    st.markdown("### Step 1: Define Shared Context")
    st.write(
    """
    You need to provide a shared context for the simulation participants. This context will be the memory shared by all players and the Game Master. It's essential to describe the background or scenario that connects all the agents in your simulation.  

    For example, if we wanted to study agents' behavior in a social network, we might provide detailed descriptions of the platform’s features, how users interact with each other, and the mechanics that drive content engagement. This could include specifying how posts gain visibility, the role of algorithms in content promotion, and the potential impact of misinformation spread. By defining these details, we ensure that all participants share a clear understanding of the simulation environment.""")

    with st.form(key="context_form"):
        # Input for shared context
        st.session_state["exp_shared_context"] = st.text_area("Write the shared context here:")

        # Buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            home_button = st.form_submit_button("Go to Dashboard", use_container_width=True)            

        with col2:
            next_pressed = st.form_submit_button("Next", use_container_width=True)

    if next_pressed:
        if not st.session_state["exp_shared_context"].strip():
            st.warning("The shared context cannot be empty. Please provide a description.")
        else:
            if not st.session_state["exp_generated_generic_knowledge"]:
                with st.spinner("Summarizing the shared context..."):
                    generic_knowledge = create_generic_knowledge(st.session_state["exp_shared_context"])

                    if generic_knowledge:
                        st.session_state["exp_generated_generic_knowledge"] = True
                        st.session_state["exp_generic_knowledge"] = generic_knowledge
                        
                        updated_agents = []
                        for agent in copy.deepcopy(st.session_state["agents"]):
                            agent["context"] = generic_knowledge  
                            updated_agents.append(agent)

                        st.session_state["exp_agents_copied"] = updated_agents

                        st.success("Shared context submitted successfully!")
            
            st.session_state["exp_step"] = 2  
            st.rerun()  
    if home_button:
        page_file = pages["Dashboard"]
        st.switch_page(page_file)

# Step 2: Input goal and agent-specific context
elif st.session_state["exp_step"] == 2:
    st.markdown("### Step 2: Define Agent Goal & Individual Context")  
    st.write(  
        "Specify the objective that will guide each agent's behavior within the simulation. "
        "Additionally, provide a unique context for each agent, defining their role and perspective within the experiment.")

    with st.form(key="goal_form"):
        agent_goals = {}
        agent_contexts = {}
        
        for agent in st.session_state["exp_agents_copied"]:
            st.markdown(f"#### {agent['name']}")  
            agent_goals[agent["name"]] = st.text_area(f"Goal for {agent['name']}:", key=f"goal_{agent['name']}")
            agent_contexts[agent["name"]] = st.text_area(f"Context for {agent['name']}:", key=f"context_{agent['name']}")
                
        col1, col2 = st.columns([1, 1])
        with col1:
            back_pressed = st.form_submit_button("Back", use_container_width=True)
        with col2:
            submit_pressed = st.form_submit_button("Begin Simulation", use_container_width=True)

        if back_pressed:
            st.session_state["exp_step"] = 1  
            st.rerun()

        if submit_pressed:
            missing_fields = any(not goal.strip() or not context.strip() for goal, context in zip(agent_goals.values(), agent_contexts.values()))

            if missing_fields:
                st.warning("Each agent must have both a goal and a context.")
            else:
                updated_agents = []
                for agent in st.session_state["exp_agents_copied"]:
                    updated_agent = agent.copy()
                    updated_agent["goal"] = agent_goals[agent["name"]]
                    updated_agent["context"] += agent_contexts[agent["name"]]
                    updated_agent["ind_context"] = agent_contexts[agent["name"]]
                    updated_agents.append(updated_agent)

                st.session_state["exp_agents_copied"] = updated_agents
                                
                st.session_state["exp_step"] = 3  
                st.success("Agent goals and contexts have been successfully set!")
                st.rerun()

# Step 3: Run the simulation
elif st.session_state["exp_step"] == 3:
    st.markdown("### Step 3: Run Simulation")
    
    if st.session_state["exp_agents_validated"] and st.session_state["exp_generated_generic_knowledge"] and not st.session_state["exp_players_built"]: 
        with st.spinner("Building players, this may take a while..."):        
            player_configs = create_player_configs(st.session_state["exp_agents_copied"])
            players, memories = build_players(player_configs)
            st.session_state["exp_players"] = players
            st.session_state["exp_memories"] = memories
            st.session_state["exp_players_built"] = True
            st.success("Players built successfully")
    
    if st.session_state["exp_players_built"] and not st.session_state["exp_gm_built"]:
        with st.spinner("Building the Game Master..."):
            st.session_state["exp_gm"] = build_gm(players=st.session_state["exp_players"], 
                                            shared_context=st.session_state["exp_generic_knowledge"])
            st.session_state["exp_gm_built"] = True
            st.success("Game Master built successfully")

    if st.session_state["exp_gm_built"]:
        episode_length = st.number_input("Enter the number of episodes", min_value=4, value=4, max_value=12, step=1)
        if st.button("Run Episodes", use_container_width=True):
            with st.spinner(f"Running {episode_length} episodes..."):
                for _ in range(episode_length):
                    st.session_state["exp_gm"].step()
                st.session_state["exp_simulation_run"] = True
                
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
            st.session_state["exp_step"] = 1  
            st.session_state["exp_players"] = []
            st.session_state["exp_memories"] = []
            st.session_state["exp_players_built"] = False
            st.session_state["exp_gm_built"] = False
            st.session_state["exp_gm"] = None
            st.session_state["exp_simulation_run"] = False
            st.session_state["exp_generated_generic_knowledge"] = False
            st.session_state["exp_agents_validated"] = False
            st.session_state["exp_shared_context"] = ""
            st.session_state["exp_agents_copied"] = []
            st.rerun()
            
    # After the confrontation simulation, show the memory logs and summaries
    if st.session_state["exp_simulation_run"]:
        st.markdown("<br>", unsafe_allow_html=True)
        summary(st.session_state["exp_gm"], st.session_state["exp_players"], st.session_state["exp_memories"])
