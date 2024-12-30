import streamlit as st


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


# Dictionary mapping page names to functions
pages = {
    "Simulations": "./pages/simulations.py",
    "Agents": "./pages/agents.py"
}


# Simulations 
st.markdown("## Simulation Area")

# Step 1: Verifying agents
if not st.session_state["agents_validated"]:
    with st.spinner("Verifying the existence of agents..."):
        if st.session_state["agents"]:
            st.session_state["agents_validated"] = True
            st.success("Agents found")
        else:
            st.error("The agents do not exist, please create them")
            _, _ , _, col1, _, _, _ = st.columns([1, 1, 1, 1, 1, 1, 1])  
            with col1:
                if st.button("Create Agents"):
                    page_file = pages["Agents"]
                    st.switch_page(page_file)

# Step 2: Building players
if st.session_state["agents_validated"] and not st.session_state["players_built"]:
    from simulations.simulation_runner import *  # Some imports take time; moved import here so that it is faster in case of inexistence of agents
    with st.spinner("Building players, this may take a while..."):
        player_configs = create_player_configs(st.session_state["agents"])
        players, memories = build_players(player_configs)
        st.session_state["players"] = players
        st.session_state["memories"] = memories
        st.session_state["players_built"] = True
        st.success("Players built successfully")

# Step 3: Building the Game Master
if st.session_state["players_built"] and not st.session_state["gm_built"]:
    with st.spinner("Building the Game Master..."):
        st.session_state["gm"] = build_gm(players=st.session_state["players"], 
                                          shared_context=st.session_state["generic_knowledge"])
        st.session_state["gm_built"] = True
        st.success("Game Master built successfully")

# Step 4: Run the simulation
if st.session_state["gm_built"]:
    episode_length = st.number_input("Enter the number of episodes", min_value=4, value=4, max_value=12, step=1)
    _, _ , _, col1, _, _, _ = st.columns([1, 1, 1, 1, 1, 1, 1])  
    with col1:
        if st.button("Run Simulation"):
            with st.spinner(f"Running {episode_length} episodes..."):
                for _ in range(episode_length):
                    st.session_state["gm"].step()
                st.session_state["simulation_run"] = True
                st.success(f"Completed {episode_length} episodes.")

# Step 5: Display Results
if st.session_state["simulation_run"]:
    st.markdown("<br>", unsafe_allow_html=True)
    summary(st.session_state["gm"], st.session_state["players"], st.session_state["memories"])


# "Go Back" Button
st.markdown("<br>", unsafe_allow_html=True)
_, _ , _, col1, _, _, _ = st.columns([1, 1, 1, 1, 1, 1, 1])  
with col1:
    home_button = st.button("Go Back", use_container_width=True)
    if home_button:
        # Switch to the selected page
        page_file = pages["Simulations"]
        st.switch_page(page_file)
