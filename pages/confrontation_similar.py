import copy
import streamlit as st
from simulations.agent_similarity import *
from simulations.simulation_runner import *
from simulations.agent_creation import create_generic_knowledge

# Page personalization
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")
st.markdown("## Agent Confrontation Based On Similarity")

# Dictionary mapping page names to functions
pages = {
    "Dashboard": "./pages/dashboard.py",
    "confrontation2": "./pages/confrontation_similar.py",
    "Agents": "./pages/agents.py",
}

# Initialize session state variables with unique prefix
if "agents" not in st.session_state:
    st.session_state["agents"] = []
if "confs_agents_validated" not in st.session_state:
    st.session_state["confs_agents_validated"] = False
if "confs_step" not in st.session_state:
    st.session_state["confs_step"] = 1  
if "confs_generated_generic_knowledge" not in st.session_state:
    st.session_state["confs_generated_generic_knowledge"] = False
if "confs_most_similar_agents" not in st.session_state:
    st.session_state["confs_most_similar_agents"] = []
if "confs_most_different_agents" not in st.session_state:
    st.session_state["confs_most_different_agents"] = []  
if "confs_players_built" not in st.session_state:
    st.session_state["confs_players_built"] = False
if "confs_gm_built" not in st.session_state:
    st.session_state["confs_gm_built"] = False
if "confs_gm_confrontation" not in st.session_state:
    st.session_state["confs_gm_confrontation"] = None
if "confs_confrontation_ready" in st.session_state:
    del st.session_state["confs_confrontation_ready"]

# Ensure "confs_agents_copied" is only created when "agents" is not empty
if "confs_agents_copied" not in st.session_state or not st.session_state["confs_agents_copied"]:
    st.session_state["confs_agents_copied"] = copy.deepcopy(st.session_state["agents"])

# Step 1: Shared Context Definition
if not st.session_state["confs_agents_validated"]:
    with st.spinner("Verifying the existence of agents..."):
        if st.session_state["agents"]:
            st.session_state["confs_agents_validated"] = True
        else:
            st.error("Agent confrontation cannot start because no agents have been defined. Please refer to the button below to create them.")
            _, col1, _ = st.columns([1, 1, 1])
            with col1:
                if st.button("Create Agents", use_container_width=True):
                    page_file = pages["Agents"]
                    st.switch_page(page_file)

if st.session_state["confs_agents_validated"] and st.session_state["confs_step"] == 1:
    st.markdown("### Step 1: Define Shared Context")
    st.write(
    """
    You need to provide a shared context for the simulation participants. This context will be the memory shared by all players and the Game Master. It's essential to describe the background or scenario that connects all the agents in your simulation.  

    For example, if we wanted to study agents' behavior in a social network, we might provide detailed descriptions of the platform’s features, how users interact with each other, and the mechanics that drive content engagement. This could include specifying how posts gain visibility, the role of algorithms in content promotion, and the potential impact of misinformation spread. By defining these details, we ensure that all participants share a clear understanding of the simulation environment.""")

    with st.form(key="confs_context_form"):
        st.session_state["confs_shared_context"] = st.text_area("Write the shared context here:")
        col1, col2 = st.columns([1, 1])
        with col1:
            home_button = st.form_submit_button("Go to Dashboard", use_container_width=True)
        with col2:
            next_pressed = st.form_submit_button("Next", use_container_width=True)
    if home_button:
        st.switch_page(pages["Dashboard"])
    if next_pressed:
        if not st.session_state["confs_shared_context"].strip():
            st.warning("The shared context cannot be empty. Please provide a description.")
        else:
            if not st.session_state["confs_generated_generic_knowledge"]:
                with st.spinner("Summarizing the shared context..."):
                    generic_knowledge = create_generic_knowledge(st.session_state["confs_shared_context"])
                    if generic_knowledge:
                        st.session_state["confs_generated_generic_knowledge"] = True
                        st.session_state["confs_generic_knowledge"] = generic_knowledge
                        updated_agents = []
                        for agent in copy.deepcopy(st.session_state["agents"]):
                            agent["context"] = generic_knowledge
                            updated_agents.append(agent)
                        st.session_state["confs_agents_copied"] = updated_agents
                        st.success("Shared context submitted successfully!")
            st.session_state["confs_step"] = 2
            st.rerun()

# Step 2: Agent Goal & Individual Context
elif st.session_state["confs_step"] == 2:
    st.markdown("### Step 2: Define Agent Goal & Individual Context")
    st.write(  
        "Specify the objective that will guide each agent's behavior within the simulation. "
        "Additionally, provide a unique context for each agent, defining their role and perspective within the experiment.")

    with st.form(key="confs_goal_form"):
        agent_goals = {}
        agent_contexts = {}
        for agent in st.session_state["confs_agents_copied"]:
            st.markdown(f"#### {agent['name']}")
            agent_goals[agent["name"]] = st.text_area(f"Goal for {agent['name']}:", key=f"goal_{agent['name']}")
            agent_contexts[agent["name"]] = st.text_area(f"Context for {agent['name']}:", key=f"context_{agent['name']}")
        col1, col2 = st.columns([1, 1])
        with col1:
            back_pressed = st.form_submit_button("Back", use_container_width=True)
        with col2:
            next_button = st.form_submit_button("Next", use_container_width=True)
        if back_pressed:
            st.session_state["confs_step"] = 1
            st.rerun()
        if next_button:
            missing_fields = any(not goal.strip() or not context.strip() for goal, context in zip(agent_goals.values(), agent_contexts.values()))
            if missing_fields:
                st.warning("Each agent must have both a goal and a context.")
            else:
                updated_agents = []
                for agent in st.session_state["confs_agents_copied"]:
                    updated_agent = agent.copy()
                    updated_agent["goal"] = agent_goals[agent["name"]]
                    updated_agent["context"] += agent_contexts[agent["name"]]
                    updated_agent["ind_context"] = agent_contexts[agent["name"]]
                    updated_agents.append(updated_agent)
                st.session_state["confs_agents_copied"] = updated_agents
                st.session_state["confs_step"] = 3
                st.success("Agent goals and contexts have been set!")
                st.rerun()

# Step 3: Set Weights for Similarity Calculation
elif st.session_state["confs_step"] == 3:
    st.markdown("### Step 3: Set Weights for Similarity Calculation")
    st.markdown(
        """
        The similarity between agents is calculated based on three components:
        - **Traits Similarity**: Measures how similar the agents are based on their personality traits (e.g., extraversion, openness).
        - **Text Similarity**: Compares the agents' goals and context to find common themes in their textual data.
        - **Ideology Similarity**: Assesses how close the agents are in terms of their political ideologies.

        You can use the sliders below to assign weights to these components, determining their relative importance in the overall similarity calculation. 
        The sum of all weights must equal 1 for the calculation to proceed.
        """)
    
    with st.form(key="confs_weights_form"):
        st.session_state["confs_traits_weight"] = st.slider("Traits Weight", min_value=0.0, max_value=1.0, value=0.7, step=0.05)
        st.session_state["confs_text_weight"] = st.slider("Text Weight", min_value=0.0, max_value=1.0, value=0.15, step=0.05)
        st.session_state["confs_ideology_weight"] = st.slider("Ideology Weight", min_value=0.0, max_value=1.0, value=0.15, step=0.05)
        col1, col2 = st.columns([1, 1])
        with col1:
            back_pressed = st.form_submit_button("Back", use_container_width=True)
        with col2:
            next_pressed = st.form_submit_button("Next", use_container_width=True)
    if back_pressed:
        st.session_state["confs_step"] = 2
        st.rerun()
    if next_pressed:
        total_weight = st.session_state["confs_traits_weight"] + st.session_state["confs_text_weight"] + st.session_state["confs_ideology_weight"]
        if total_weight != 1.0:
            st.warning("The sum of the weights must equal 1. Please adjust the values.")
        else:
            st.session_state["confs_step"] = 4
            st.rerun()

# Step 4: Comparison Method Selection
elif st.session_state["confs_step"] == 4:
    st.markdown("### Step 4: Comparison Method Selection")
    with st.form(key="confs_comparison_form"):
        st.session_state["confs_selected_pair"] = st.radio(
            "Choose the comparison method:",
            options=[
                "Using Local Functions",
                "Using Provided LLM"
            ]
        )
        col1, col2 = st.columns([1, 1])
        with col1:
            back_pressed = st.form_submit_button("Back", use_container_width=True)
        with col2:
            next_pressed = st.form_submit_button("Next", use_container_width=True)
        if back_pressed:
            st.session_state["confs_step"] = 3
            st.rerun()
        if next_pressed:
            st.session_state["confs_step"] = 5
            st.rerun()

# Step 5: Confrontation Setup
elif st.session_state["confs_step"] == 5:
    st.markdown("### Step 5: Confrontation Setup")
    with st.spinner("Calculating agent similarities..."):
        if "Using Local Functions" in st.session_state["confs_selected_pair"]:
            similarity_matrix = compute_agent_similarity(
                st.session_state["confs_agents_copied"],
                traits_weight=st.session_state["confs_traits_weight"],
                text_weight=st.session_state["confs_text_weight"],
                ideology_weight=st.session_state["confs_ideology_weight"],
                method="local"
            )
            most_similar, most_different = find_extreme_agents(similarity_matrix, st.session_state["confs_agents_copied"])
            agent_names = [agent["name"] for agent in st.session_state["confs_agents_copied"]]
            most_similar_agents = (agent_names[most_similar[0]], agent_names[most_similar[1]])
            most_different_agents = (agent_names[most_different[0]], agent_names[most_different[1]])
        else:
            similarity_matrix = compute_agent_similarity(
                st.session_state["confs_agents_copied"],
                traits_weight=st.session_state["confs_traits_weight"],
                text_weight=st.session_state["confs_text_weight"],
                ideology_weight=st.session_state["confs_ideology_weight"],
                method="llm"
            )
            parts = similarity_matrix.split("Most Different:")
            most_similar_part = parts[0].replace("Most Similar:", "").strip()
            most_similar_agents = [name.strip() for name in most_similar_part.split(",")]
            most_different_part = parts[1].strip()
            most_different_agents = [name.strip() for name in most_different_part.split(",")]
    st.session_state["confs_most_similar_agents"] = most_similar_agents
    st.session_state["confs_most_different_agents"] = most_different_agents
    st.session_state["confs_confrontation_ready"] = True
    with st.form(key="confs_pair_selection"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Most Similar Pair")
            st.write(f"{most_similar_agents[0]} and {most_similar_agents[1]}")
        with col2:
            st.markdown("#### Most Different Pair")
            st.write(f"{most_different_agents[0]} and {most_different_agents[1]}")
        selected_pair = st.radio(
            "Select the pair for confrontation:",
            options=[
                f"Most Similar Pair: {most_similar_agents[0]} and {most_similar_agents[1]}",
                f"Most Different Pair: {most_different_agents[0]} and {most_different_agents[1]}"
            ]
        )
        col3, col4 = st.columns([1, 1])
        with col3:
            back_pressed = st.form_submit_button("Back", use_container_width=True)
        with col4:
            begin_simulation = st.form_submit_button("Begin Simulation", use_container_width=True)
        if back_pressed:
            st.session_state["confs_step"] = 4
            st.rerun()
        if begin_simulation:
            if "Most Similar Pair" in selected_pair:
                confs_player1, confs_player2 = st.session_state["confs_most_similar_agents"]
            else:
                confs_player1, confs_player2 = st.session_state["confs_most_different_agents"]
            st.session_state["confs_player1"] = confs_player1
            st.session_state["confs_player2"] = confs_player2
            st.session_state["confs_step"] = 6
            st.rerun()

# Step 6: Run Simulation
elif st.session_state["confs_step"] == 6:
    st.markdown("### Step 6: Run Simulation")
    
    # Create players and memories
    if st.session_state["confs_generated_generic_knowledge"] and not st.session_state["confs_players_built"]:
        with st.spinner("Building players, this may take a while..."):
            player_configs = create_player_configs(st.session_state["confs_agents_copied"])
            players, memories = build_players(player_configs)
            st.session_state["confs_players_confrontation"] = players
            st.session_state["confs_memories_confrontation"] = memories
            st.session_state["confs_players_built"] = True
            st.success("Players built successfully")
    
    # Build the Game Master
    if st.session_state["confs_players_built"] and not st.session_state["confs_gm_built"]:
        selected_players = [
            player for player in st.session_state["confs_players_confrontation"]
            if player.name in [st.session_state["confs_player1"], st.session_state["confs_player2"]]
        ]
        with st.spinner("Building Game Master for confrontation..."):
            confrontation_premise = f"{st.session_state['confs_player1']} and {st.session_state['confs_player2']} are in a conversation."
            st.session_state["confs_gm_confrontation"] = build_gm(
                players=selected_players,
                shared_context=st.session_state.get("confs_generic_knowledge", "") + " " + confrontation_premise
            )
            st.session_state["confs_gm_built"] = True
            st.success("Game Master built successfully!")
    
    # Run the simulation episodes
    if st.session_state["confs_gm_built"]:
        st.markdown("<br>", unsafe_allow_html=True)
        episode_length = st.number_input("Enter the number of episodes", min_value=1, value=4, max_value=12, step=1)
        if st.button("Run Episodes", use_container_width=True):
            with st.spinner(f"Running {episode_length} episodes..."):
                for _ in range(episode_length):
                    st.session_state["confs_gm_confrontation"].step()
                st.session_state["confs_simulation_completed"] = True

    # Navigation buttons
    _, col1, col2, _ = st.columns([1, 1, 1, 1])
    with col1:
        if st.button("Go to Dashboard", use_container_width=True):
            st.switch_page(pages["Dashboard"])
    with col2:
        if st.button("New Simulation", use_container_width=True):
            st.session_state["confs_step"] = 1
            st.session_state["confs_players_confrontation"] = []
            st.session_state["confs_memories_confrontation"] = []
            st.session_state["confs_players_built"] = False
            st.session_state["confs_gm_built"] = False
            st.session_state["confs_gm_confrontation"] = None
            st.session_state["confs_simulation_completed"] = False
            st.session_state["confs_generated_generic_knowledge"] = False
            st.session_state["confs_shared_context"] = ""
            st.rerun()
    
    # Display summary after simulation completes
    if "confs_simulation_completed" in st.session_state and st.session_state["confs_simulation_completed"]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Summary of the Confrontation:")
        selected_player = st.selectbox(
            "Select Player for Memory Log:",
            options=[st.session_state["confs_player1"], st.session_state["confs_player2"]]
        )
        if selected_player:
            player_memories = st.session_state["confs_memories_confrontation"].get(selected_player, [])
            summary(
                st.session_state.get("confs_gm_confrontation"),
                [player for player in st.session_state["confs_players_confrontation"] if player.name == selected_player],
                {selected_player: player_memories},
                selected_player=selected_player)
