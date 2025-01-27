import copy
import streamlit as st
from simulations.simulation_runner import *
from simulations.agent_similarity import *


# Page personalization
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")
st.markdown("## Agent Confrontation Based On Similarity")


# Dictionary mapping page names to functions
pages = {
    "Dashboard": "./pages/dashboard.py",
    "confrontation2": "./pages/confrontation_similar.py",
    "Agents": "./pages/agents.py",
}


# Rest variables
if "confrontation_ready" in st.session_state:
    del st.session_state["confrontation_ready"]
                

# Ensure players and memories are only built once (not every reload)
if "agents" in st.session_state and st.session_state["agents"]:
    st.markdown("### Set Weights for Similarity Calculation")
    st.markdown(
        """
        The similarity between agents is calculated based on three components:
        - **Traits Similarity**: Measures how similar the agents are based on their personality traits (e.g., extraversion, openness).
        - **Text Similarity**: Compares the agents' goals and context to find common themes in their textual data.
        - **Ideology Similarity**: Assesses how close the agents are in terms of their political ideologies.

        You can use the sliders below to assign weights to these components, determining their relative importance in the overall similarity calculation. 
        The sum of all weights must equal 1 for the calculation to proceed.
        """
    )
    traits_weight = st.slider("Traits Weight", min_value=0.0, max_value=1.0, value=0.7, step=0.05)
    text_weight = st.slider("Text Weight", min_value=0.0, max_value=1.0, value=0.15, step=0.05)
    ideology_weight = st.slider("Ideology Weight", min_value=0.0, max_value=1.0, value=0.15, step=0.05)
    
    if traits_weight + text_weight + ideology_weight != 1.0:
        st.error("The sum of the weights must equal 1. Please adjust the values.")
    else: 
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Comparison Method Selection")
        with st.form(key="agent_comparison_option"):
            selected_pair = st.radio(
            "Choose the comparison method:",
            options=[
                "Using Local Functions",
                "Using Provided LLM"]
            )

            submitted = st.form_submit_button("Proceed")
        
        if submitted:
            with st.spinner("Calculating agent similarities..."):
                if "Using Local Functions" in selected_pair:
                    similarity_matrix = compute_agent_similarity(
                        st.session_state["agents"],
                        traits_weight=traits_weight,
                        text_weight=text_weight,
                        ideology_weight=ideology_weight,
                        method="local",
                    )
                    most_similar, most_different = find_extreme_agents(similarity_matrix, st.session_state["agents"])
                    agent_names = [agent["name"] for agent in st.session_state["agents"]]
                    most_similar_agents = (agent_names[most_similar[0]], agent_names[most_similar[1]])
                    most_different_agents = (agent_names[most_different[0]], agent_names[most_different[1]])
                else:
                    similarity_matrix = compute_agent_similarity(
                        st.session_state["agents"],
                        traits_weight=traits_weight,
                        text_weight=text_weight,
                        ideology_weight=ideology_weight,
                        method="llm",
                    )

                    # Split the string into two parts
                    parts = similarity_matrix.split("Most Different:")

                    # Extract the "Most Similar" pair
                    most_similar_part = parts[0].replace("Most Similar:", "").strip()
                    most_similar_agents = [name.strip() for name in most_similar_part.split(",")]

                    # Extract the "Most Different" pair
                    most_different_part = parts[1].strip()
                    most_different_agents = [name.strip() for name in most_different_part.split(",")]
            
            st.session_state["confrontation_ready"] = True

            col1, col2 = st.columns(2)
            # Display the most similar pair
            with col1:
                st.markdown("### Most Similar Pair")
                st.write(f"{most_similar_agents[0]} and {most_similar_agents[1]}")

            # Display the most different pair
            with col2:
                st.markdown("### Most Different Pair")
                st.write(f"{most_different_agents[0]} and {most_different_agents[1]}")
else:
    st.error("Agent confrontation cannot start because no agents have been defined. Please refer to the button below to create them.")
    _, _, _, col1, _, _, _ = st.columns([1, 1, 1, 1, 1, 1, 1])  
    with col1:
        if st.button("Create Agents", use_container_width=True):
            # Switch to the selected page
            page_file = pages["Agents"]
            st.switch_page(page_file)

    
# Separate condition for confrontation logic
if st.session_state.get("confrontation_ready"):
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Confrontation Setup")
    with st.form(key="interaction_goal_form"):
        # Select pair for confrontation
        selected_pair = st.radio(
            "Select the pair for confrontation:",
            options=[
                f"Most Similar Pair: {most_similar_agents[0]} and {most_similar_agents[1]}",
                f"Most Different Pair: {most_different_agents[0]} and {most_different_agents[1]}",
            ],
        )

        interaction_goal = st.text_area(
            "Specify the goal of the interaction:",
            placeholder="e.g., Discuss about the impact of fake news in social media.",
        )

        submitted = st.form_submit_button("Submit")

    if submitted:
        # Reset session state for confrontation-specific elements
        for key in ["players_confrontation2", "memories_confrontation2", "gm_confrontation2"]:
            st.session_state.pop(key, None)

        # Extract players based on selected pair
        if "Most Similar Pair" in selected_pair:
            player1, player2 = st.session_state["most_similar_agents"]
        else:
            player1, player2 = st.session_state["most_different_agents"]

        st.session_state["player1"] = player1
        st.session_state["player2"] = player2

        if not interaction_goal:
            st.error("Please specify the goal of the interaction before proceeding.")
        else:
            # Update agent goals
            agents_copy = copy.deepcopy(st.session_state.get("updated_agents", st.session_state["agents"]))
            for agent in agents_copy:
                if agent["name"] in [player1, player2]:
                    agent["goal"] = interaction_goal
                    agent["context"] = interaction_goal

            # Build players and memories
            with st.spinner("Building players and memories, this may take a while..."):
                player_configs = create_player_configs(agents_copy)
                players, memories = build_players(player_configs)
                st.session_state["players_confrontation2"] = players
                st.session_state["memories_confrontation2"] = memories

            # Select players for the confrontation
            selected_players = [
                player for player in st.session_state["players_confrontation2"]
                if player.name in [player1, player2]
            ]

            # Build the Game Master for the confrontation
            with st.spinner("Building Game Master for confrontation..."):
                confrontation_premise = f"{player1} and {player2} are in a conversation. The goal of their interaction is: {interaction_goal}."
                st.session_state["gm_confrontation2"] = build_gm(
                    players=selected_players,
                    shared_context=st.session_state.get("generic_knowledge", "") + " " + confrontation_premise,
                )
                st.success("Game Master built successfully!")
                    

# Buttons for navigation
_, _ , col1, _, _ = st.columns([1, 1, 1, 1, 1])  
with col1:
    home_button = st.button("Go Back", use_container_width=True)
    if home_button:
        # Switch to the selected page
        page_file = pages["Dashboard"]
        st.switch_page(page_file)
        

# After the confrontation simulation, show the memory logs and summaries
st.markdown("<br>", unsafe_allow_html=True)
if "simulation_completed2" in st.session_state and st.session_state["simulation_completed2"] is not None:
    # Extract player names dynamically from the session state
    confronted_player_names = [st.session_state["player1"], st.session_state["player2"]]

    # Extract player names for memory log display
    selected_player = st.selectbox("Select Player for Memory Log:", options=confronted_player_names)

    # Only show the memory log and summary after the confrontation is done
    if selected_player:
        st.markdown(f"### {selected_player}'s Summary:")
        player_memories = st.session_state["memories_confrontation2"].get(selected_player, [])
        summary(st.session_state.get("gm_confrontation2"), 
                [player for player in st.session_state["players_confrontation2"] if player.name == selected_player], 
                {selected_player: player_memories}, 
                selected_player=selected_player)
