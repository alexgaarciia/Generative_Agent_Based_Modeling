import streamlit as st
from simulations.simulation_runner import create_generic_knowledge
from simulations.simulation_runner import create_player_configs

st.set_page_config(layout="centered", initial_sidebar_state="collapsed")


# Dictionary mapping page names to functions
pages = {
    "Simulations": "./pages/simulations.py",
}


# Simulations 
st.markdown("## Simulation Area")
st.markdown("### Shared Context")
st.markdown(
    """
    In this section, you can provide a shared context for the simulation participants. 
    This context will be the memory shared by all players and the Game Master. 
    It's essential to describe the background or scenario that connects all the agents in your simulation.
    """
)


# Form for shared context
with st.form("shared_context_form"):
    shared_context = st.text_area(
        "Please write the shared context here:",
        help="This context will serve as a common background for all participants in the simulation.",
    )
    submit_button = st.form_submit_button("Submit")

    if submit_button:
        if not shared_context.strip():
            st.warning("The shared context cannot be empty. Please provide a description.")
        else:
            st.success("Shared context submitted successfully!")
            st.session_state["shared_context"] = shared_context
            st.write(create_generic_knowledge(shared_context))
            st.write(create_player_configs(st.session_state.agents))
    

# Buttons
home_button = st.button("Go Back")
if home_button:
    page_file = pages["Simulations"]
    st.switch_page(page_file)
