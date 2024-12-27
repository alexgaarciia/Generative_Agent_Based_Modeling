import streamlit as st
from simulations.simulation_runner import build_gm

st.set_page_config(layout="centered", initial_sidebar_state="collapsed")


# Dictionary mapping page names to functions
pages = {
    "Confrontation Main Page": "./pages/confrontation.py",
    "Agents": "./pages/agents.py",
}


# Simulation Configuration
st.markdown("## Interact with Specific Agents")
if "agents" in st.session_state and st.session_state["agents"]:
    with st.form("confrontation_form"):
        # Extract player names from session state
        player_names = [agent["name"] for agent in st.session_state["agents"]]

        # Selectbox for player1
        player1 = st.selectbox("Select Player 1:", options=player_names)

        # Selectbox for player2
        player2_options = [name for name in player_names if name != player1]
        player2 = st.selectbox("Select Player 2:", options=player2_options)

        # Text area to specify the goal of the interaction
        interaction_goal = st.text_area("Specify the goal of the interaction:", placeholder="e.g., Discuss about the impact of fake news in social media.")

        # Submit Button
        submitted = st.form_submit_button("Submit")

        if submitted:
            st.success(f"You have selected {player1} and {player2} for confrontation.")
            #confrontation_premise = f"{player1} and {player2} are in a conversation. The goal of their interaction is: {interaction_goal}."
            #st.session_state["gm2"] = build_gm(players=st.session_state["players"], shared_context=confrontation_premise)
            #st.session_state["gm2"].step()  
else:
    st.error("Agent confrontation cannot start because no agents have been defined. Please refer to the button below to create them.")
    _, _ , _, col1, _, _, _ = st.columns([1, 1, 1, 1, 1, 1, 1])  
    with col1:
        if st.button("Create Agents", use_container_width=True):
            # Switch to the selected page
            page_file = pages["Agents"]
            st.switch_page(page_file)


# Buttons
st.markdown("<br>", unsafe_allow_html=True)
_, _ , _, col1, _, _, _ = st.columns([1, 1, 1, 1, 1, 1, 1])  
with col1:
    home_button = st.button("Go Back", use_container_width=True)
    if home_button:
        # Switch to the selected page
        page_file = pages["Confrontation Main Page"]
        st.switch_page(page_file)
