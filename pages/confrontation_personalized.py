import copy
import streamlit as st

# Page personalization
st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

# Initialize session state variables for steps
if "confp_player_names" not in st.session_state:
    st.session_state["confp_player_names"] = []
if "agents" not in st.session_state:
    st.session_state["agents"] = []
if "confp_step" not in st.session_state:
    st.session_state["confp_step"] = 1  
if "confp_players_built" not in st.session_state:
    st.session_state["confp_players_built"] = False
if "confp_gm_confrontation" not in st.session_state:
    st.session_state["confp_gm_confrontation"] = None 
if "confp_gm_built" not in st.session_state:
    st.session_state["confp_gm_built"] = False
if "confp_simulation_completed" not in st.session_state:
    st.session_state["confp_simulation_completed"] = False

# Dictionary mapping page names to functions
pages = {
    "Dashboard": "./pages/dashboard.py",
    "Agents": "./pages/agents.py",
}

# Simulation Configuration
st.markdown("## Interact with Specific Agents")

# Ensure players and memories are only built once (not every reload)
if "agents" in st.session_state and st.session_state["agents"]:
    from simulations.simulation_runner import *
    from simulations.agent_creation import create_generic_knowledge
    
    # Step 1: Select Players and Set Interaction Goal
    if st.session_state["confp_step"] == 1:
        st.markdown("### Summary of Agents")
        
        # Loop over the agents and display them in collapsible sections
        for agent in st.session_state["agents"]:
            with st.expander(f"{agent['name']}"):  
                st.markdown(f"**Gender**: {agent['gender']}")
                st.markdown(f"**Political Ideology**: {agent['political_ideology']}")
                st.markdown("**Traits:**")
                for trait, value in agent["traits"].items():
                    st.markdown(f"- **{trait.capitalize()}**: {value}")
                    
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Step 1: Select Agents To Confront")
        with st.form("confrontation_form"):
            # Extract player names from session state
            st.session_state["confp_player_names"] = [agent["name"] for agent in st.session_state["agents"]]

            # Selectbox for player1
            confp_player1 = st.selectbox("Select Player 1:", options=st.session_state["confp_player_names"])

            # Selectbox for player2
            confp_player2 = st.selectbox("Select Player 2:", options=st.session_state["confp_player_names"])

            # Buttons
            col1, col2 = st.columns([1, 1])
            with col1:
                # "Go to Dashboard" button
                home_button = st.form_submit_button("Go to Dashboard", use_container_width=True)            

            with col2:
                # "Next" button
                next_pressed = st.form_submit_button("Next", use_container_width=True)

        if home_button:
            # Switch to the selected page
            page_file = pages["Dashboard"]
            st.switch_page(page_file)
            
        if next_pressed:
            if confp_player1 == confp_player2:
                st.warning("Player 1 and Player 2 cannot be the same. Please select different characters.")
            else:
                # Store selected players and their interaction goal
                st.session_state["confp_player1"] = confp_player1
                st.session_state["confp_player2"] = confp_player2
                
                selected_players = [st.session_state["confp_player1"], st.session_state["confp_player2"]]
                st.session_state["confp_agents_copied"] = [
                    copy.deepcopy(agent) for agent in st.session_state["agents"] if agent["name"] in selected_players]
                
                st.session_state["confp_step"] = 2  # Move to Step 2
                st.rerun()  # Ensures the UI updates immediately

    # Step 2: Define Shared Context
    elif st.session_state["confp_step"] == 2:
        st.markdown("### Step 2: Define Shared Context")
        st.write(
        """
        You need to provide a shared context for the simulation participants. This context will be the memory shared by all players and the Game Master. It's essential to describe the background or scenario that connects all the agents in your simulation.  

        For example, if we wanted to study agents' behavior in a social network, we might provide detailed descriptions of the platform’s features, how users interact with each other, and the mechanics that drive content engagement. This could include specifying how posts gain visibility, the role of algorithms in content promotion, and the potential impact of misinformation spread. By defining these details, we ensure that all participants share a clear understanding of the simulation environment.""")

        with st.form(key="context_form"):
            # Input for shared context
            st.session_state["confp_shared_context"] = st.text_area("Write the shared context here:")

            # Buttons
            col1, col2 = st.columns([1, 1])
            with col1:
                # "Go Back" button
                back_pressed = st.form_submit_button("Go Back", use_container_width=True)

            with col2:
                # "Next" button
                next_pressed = st.form_submit_button("Next", use_container_width=True)

        if back_pressed:
            st.session_state["confp_step"] = 1  # Go back to Step 1
            st.rerun()
            
        if next_pressed:
            if not st.session_state["confp_shared_context"].strip():
                st.warning("The shared context cannot be empty. Please provide a description.")
            else:
                # Generate the shared context for agents and the GM
                if not st.session_state.get("confp_generated_generic_knowledge"):
                    with st.spinner("Summarizing the shared context..."):
                        generic_knowledge = create_generic_knowledge(st.session_state["confp_shared_context"])

                        if generic_knowledge:
                            st.session_state["confp_generated_generic_knowledge"] = True
                            st.session_state["confp_generic_knowledge"] = generic_knowledge
                            for agent in st.session_state["confp_agents_copied"]:
                                agent["context"] = generic_knowledge
                            st.success("Shared context submitted successfully!")

                st.session_state["confp_step"] = 3  # Move to Step 3
                st.rerun()  # Ensures the UI updates immediately

    # Step 3: Input agent goals and context
    elif st.session_state["confp_step"] == 3:
        st.markdown("### Step 3: Define Agent Goal & Individual Context")  
        st.write("""
        Specify the objective that will guide each agent's behavior within the simulation.
        Additionally, provide a unique context for each agent, defining their role and perspective within the experiment.
        """)

        with st.form(key="goal_form"):
            agent_goals = {}
            agent_contexts = {}

            for agent in st.session_state["confp_agents_copied"]:
                st.markdown(f"#### {agent['name']}")  
                agent_goals[agent["name"]] = st.text_area(f"Goal for {agent['name']}:", key=f"goal_{agent['name']}")
                agent_contexts[agent["name"]] = st.text_area(f"Context for {agent['name']}:", key=f"context_{agent['name']}")
                    
            col1, col2 = st.columns([1, 1])
            with col1:
                back_pressed = st.form_submit_button("Back", use_container_width=True)
            with col2:
                submit_pressed = st.form_submit_button("Begin Simulation", use_container_width=True)

            if back_pressed:
                st.session_state["confp_step"] = 2  # Go back to Step 2
                st.rerun()

            if submit_pressed:
                missing_fields = any(not goal.strip() or not context.strip() for goal, context in zip(agent_goals.values(), agent_contexts.values()))

                if missing_fields:
                    st.warning("Each agent must have both a goal and a context.")
                else:                    
                    # Save goal and context
                    for agent in st.session_state["confp_agents_copied"]:
                        agent["goal"] = agent_goals[agent["name"]]
                        agent["context"] += agent_contexts[agent["name"]]
                        agent["ind_context"] = agent_contexts[agent["name"]]

                    st.session_state["confp_step"] = 4  # Move to Step 4
                    st.success("Agent goals and contexts have been successfully set!")
                    st.rerun()

    # Step 4: Begin the simulation
    elif st.session_state["confp_step"] == 4:
        st.markdown("### Step 4: Run Simulation")
        
        # Create players and memories
        if st.session_state["confp_generated_generic_knowledge"] and not st.session_state["confp_players_built"]: 
            with st.spinner("Building players, this may take a while..."):        
                # Create players and memories
                player_configs = create_player_configs(st.session_state["confp_agents_copied"])
                players, memories = build_players(player_configs)
                st.session_state["confp_players_confrontation"] = players
                st.session_state["confp_memories_confrontation"] = memories
                st.session_state["confp_players_built"] = True
                st.success("Players built successfully")
                
        # Build the Game Master
        if st.session_state["confp_players_built"] and not st.session_state["confp_gm_built"]:                
            # Select the new players
            selected_players = [player for player in st.session_state["confp_players_confrontation"] if player.name in [st.session_state["confp_player1"], st.session_state["confp_player2"]]]
            
            # Build Game Master for the new confrontation
            with st.spinner("Building Game Master for confrontation..."):
                confrontation_premise = f"{st.session_state['confp_player1']} and {st.session_state['confp_player2']} are in a conversation."
                st.session_state["confp_gm_confrontation"] = build_gm(
                    players=selected_players, 
                    shared_context=st.session_state.get("confp_generic_knowledge", "") + " " + confrontation_premise)
                st.session_state["confp_gm_built"] = True
                st.success("Game Master built successfully!")
                
        # Run the simulation
        if st.session_state["confp_gm_built"]:
            st.markdown("<br>", unsafe_allow_html=True)
            episode_length = st.number_input("Enter the number of episodes", min_value=1, value=4, max_value=12, step=1)

            if episode_length < 4:
                st.warning("Number of episodes must be at least 4 to proceed with the simulation.")
            else:
                if st.button("Run Episodes", use_container_width=True):
                    with st.spinner(f"Running {episode_length} episodes..."):
                        for _ in range(episode_length):
                            st.session_state["confp_gm_confrontation"].step()
                        st.session_state["confp_simulation_completed"] = True
                    
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
                st.session_state["confp_step"] = 1
                st.session_state["confp_players_confrontation"] = []  
                st.session_state["confp_memories_confrontation"] = []
                st.session_state["confp_players_built"] = False
                st.session_state["confp_gm_built"] = False
                st.session_state["confp_gm_confrontation"] = None
                st.session_state["confp_simulation_completed"] = False
                st.session_state["confp_generated_generic_knowledge"] = False
                st.session_state["confp_shared_context"] = ""
                st.rerun()  
    
        # After the confrontation simulation, show the memory logs and summaries
        if st.session_state.get("confp_simulation_completed"):
            st.markdown("<br>", unsafe_allow_html=True)

            # Extract player names for memory log display
            st.markdown("### Summary of the Confrontation:")
            selected_player = st.selectbox("Select Player for Memory Log:", options=[st.session_state["confp_player1"], st.session_state["confp_player2"]])

            # Only show the memory log and summary after the confrontation is done
            if selected_player:
                player_memories = st.session_state["confp_memories_confrontation"].get(selected_player, [])

                # Show summary below memory log
                summary(st.session_state.get("confp_gm_confrontation"), [player for player in st.session_state["confp_players_confrontation"] if player.name == selected_player], {selected_player: player_memories}, selected_player=selected_player)

else:
    st.error("Agent confrontation cannot start because no agents have been defined. Please refer to the button below to create them.")
    _, _ , col1, _, _ = st.columns([1, 1, 1, 1, 1])  
    with col1:
        if st.button("Create Agents", use_container_width=True):
            # Switch to the selected page
            page_file = pages["Agents"]
            st.switch_page(page_file)
