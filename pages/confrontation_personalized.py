import streamlit as st
from simulations.simulation_runner import *

st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

# Initialize the "new_simulation" key if it doesn't exist
if "new_simulation" not in st.session_state:
    st.session_state["new_simulation"] = False

# Dictionary mapping page names to functions
pages = {
    "Confrontation Main Page": "./pages/confrontation.py",
    "confrontation1": "./pages/confrontation_personalized.py",
    "Agents": "./pages/agents.py",
}

# Simulation Configuration
st.markdown("## Interact with Specific Agents")

# Reset simulation when "New Simulation" is clicked
if "new_simulation" in st.session_state and st.session_state["new_simulation"]:
    st.session_state["players_confrontation"] = None
    st.session_state["memories_confrontation"] = None
    st.session_state["gm_confrontation"] = None
    st.session_state["new_simulation"] = False  

# Ensure players and memories are only built once (not every reload)
if "agents" in st.session_state and st.session_state["agents"]:
    # Only rebuild players and memories if they haven't been created already
    if "players_confrontation" not in st.session_state or "memories_confrontation" not in st.session_state:
        with st.spinner("Building players and memories, this may take a while..."):
            player_configs = create_player_configs(st.session_state["agents"])
            players, memories = build_players(player_configs)
            st.session_state["players_confrontation"] = players
            st.session_state["memories_confrontation"] = memories
            st.success("Players and memories built successfully!")

    with st.form("confrontation_form"):
        # Extract player names from session state
        player_names = [agent["name"] for agent in st.session_state["agents"]]

        # Selectbox for player1
        player1 = st.selectbox("Select Player 1:", options=player_names)

        # Selectbox for player2
        player2 = st.selectbox("Select Player 2:", options=player_names)

        # Text area to specify the goal of the interaction
        interaction_goal = st.text_area("Specify the goal of the interaction:", placeholder="e.g., Discuss about the impact of fake news in social media.")

        # Submit Button
        submitted = st.form_submit_button("Submit")

        if submitted:
            if player1 == player2:
                st.error("Player 1 and Player 2 cannot be the same. Please select different characters.")
            elif not interaction_goal:
                st.error("Please specify the goal of the interaction before proceeding.")
            else:
                st.success(f"You have selected {player1} and {player2} for confrontation.")

                # Filter selected players
                selected_players = [player for player in st.session_state["players_confrontation"] if player.name in [player1, player2]]

                # Build a new Game Master for this confrontation only if necessary
                if "gm_confrontation" not in st.session_state or st.session_state["gm_confrontation"] is None:
                    with st.spinner("Building Game Master for confrontation..."):
                        confrontation_premise = f"{player1} and {player2} are in a conversation. The goal of their interaction is: {interaction_goal}."
                        st.session_state["gm_confrontation"] = build_gm(
                            players=selected_players, 
                            shared_context=st.session_state.get("generic_knowledge", "") + " " + confrontation_premise
                        )
                        st.success("Game Master for confrontation built successfully!")

                # Run the simulation only after Game Master is built and if it's not a new simulation
                if st.session_state.get("gm_confrontation") and not st.session_state["new_simulation"]:
                    with st.spinner("Running confrontation simulation..."):
                        st.session_state["gm_confrontation"].step()
                        st.success("Confrontation simulation completed!")
                        st.markdown("<br>", unsafe_allow_html=True)

else:
    st.error("Agent confrontation cannot start because no agents have been defined. Please refer to the button below to create them.")
    _, _ , _, col1, _, _, _ = st.columns([1, 1, 1, 1, 1, 1, 1])  
    with col1:
        if st.button("Create Agents", use_container_width=True):
            # Switch to the selected page
            page_file = pages["Agents"]
            st.switch_page(page_file)


# After the confrontation simulation, show the memory logs and summaries
st.markdown("<br>", unsafe_allow_html=True)
if "memories_confrontation" in st.session_state and st.session_state["memories_confrontation"] is not None:
    # Extract player names for memory log display
    selected_player = st.selectbox("Select Player for Memory Log:", options=player_names)

    # Only show the memory log and summary after the confrontation is done
    if selected_player:
        player_memories = st.session_state["memories_confrontation"].get(selected_player, [])

        # Show summary below memory log
        st.markdown("### Summary of the Confrontation:")
        summary(st.session_state.get("gm_confrontation"), [player for player in st.session_state["players_confrontation"] if player.name == selected_player], {selected_player: player_memories}, selected_player=selected_player)


# Buttons for navigation
st.markdown("<br>", unsafe_allow_html=True)
_, _ , col1, col2, _, _ = st.columns([1, 1, 1, 1, 1, 1])  

with col1:
    home_button = st.button("Go Back", use_container_width=True)
    if home_button:
        # Switch to the selected page
        page_file = pages["Confrontation Main Page"]
        st.switch_page(page_file)

with col2:
    if st.button("New Confrontation", use_container_width=True):
        # Mark new simulation flag and reload the page
        st.session_state["new_simulation"] = True
        page_file = pages["confrontation1"]
        st.switch_page(page_file)
