import copy
import streamlit as st
from simulations.simulation_runner import * 
from simulations.agent_creation import create_generic_knowledge



# Page personalization
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")


# Initialize session state variables
st.session_state["generated_generic_knowledge"] = False
if "begin_simulation" not in st.session_state:
    st.session_state["begin_simulation"] = False
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


# Dictionary mapping page names to functions
pages = {
    "Dashboard": "./pages/dashboard.py",
    "Agents": "./pages/agents.py"
}


# Verify existence of agents
# Ensure agents_copied exists before use (without modifying session state)
agents_copied = copy.deepcopy(st.session_state.get("agents", []))

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


# Input shared context and interaction goal
if st.session_state["agents_validated"]:
    st.markdown("### Define Shared Context & Interaction Goal")
    st.write(
    """
    You need to provide a shared context for the simulation participants. This context will be the memory shared by all players and the Game Master. It's essential to describe the background or scenario that connects all the agents in your simulation.  

    For example, if we wanted to study agents' behavior in a social network, we might provide detailed descriptions of the platform’s features, how users interact with each other, and the mechanics that drive content engagement. This could include specifying how posts gain visibility, the role of algorithms in content promotion, and the potential impact of misinformation spread. By defining these details, we ensure that all participants share a clear understanding of the simulation environment.
    
    Next, define the interaction goal to specify the objective of the agent interactions within the simulation.
    """
    )

    # Input for shared context
    shared_context = st.text_area("Please write the shared context here:")
        
    # Input for interaction goal
    interaction_goal = st.text_area("Please write the goal of the interaction here:",
                                    placeholder="e.g., Discuss about the impact of fake news in social media.")


# Allow to start the simulation
if st.button("Begin Simulation", use_container_width=True):
    if not shared_context.strip():
        st.warning("The shared context cannot be empty. Please provide a description.")
    elif not interaction_goal.strip():
        st.warning("The interaction goal cannot be empty. Please specify a goal.") 
    else:
        if not st.session_state["generated_generic_knowledge"]:
            with st.spinner("Summarizing the shared context..."):
                st.session_state["shared_context"] = shared_context
                generic_knowledge = create_generic_knowledge(shared_context)

                if generic_knowledge:
                    st.session_state["generated_generic_knowledge"] = True
                    st.session_state["generic_knowledge"] = generic_knowledge
                    for agent in agents_copied:
                        agent["context"] = generic_knowledge 
                        agent["goal"] = interaction_goal           
                    st.success("Shared context and goal submitted successfully!")
    st.session_state["begin_simulation"] = True


# Create players and memories
if st.session_state["begin_simulation"] and st.session_state["agents_validated"] and st.session_state["generated_generic_knowledge"] and not st.session_state["players_built"]: 
    with st.spinner("Building players, this may take a while..."):        
        # Create players and memories
        player_configs = create_player_configs(agents_copied)
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


# "Go Back" Button
_, _ , col1, _, _ = st.columns([1, 1, 1, 1, 1])  
with col1:
    home_button = st.button("Go Back", use_container_width=True)
    if home_button:
        # Switch to the selected page
        page_file = pages["Dashboard"]
        st.switch_page(page_file)


# After the confrontation simulation, show the memory logs and summaries
if st.session_state["simulation_run"]:
    st.markdown("<br>", unsafe_allow_html=True)
    summary(st.session_state["gm"], st.session_state["players"], st.session_state["memories"])
