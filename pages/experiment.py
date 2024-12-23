import streamlit as st
from simulations.simulation_runner import *

st.set_page_config(layout="centered", initial_sidebar_state="collapsed")


# Dictionary mapping page names to functions
pages = {
    "Simulations": "./pages/simulations.py",
}


# Simulations 
st.markdown("## Simulation Area")
st.write(st.session_state.agents)
player_configs = create_player_configs(st.session_state.agents)
#st.write(create_player_configs(st.session_state.agents))
st.write(build_players(player_configs))
    

# Buttons
home_button = st.button("Go Back")
if home_button:
    page_file = pages["Simulations"]
    st.switch_page(page_file)
