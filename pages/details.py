import streamlit as st

# Dictionary mapping page names to functions
pages = {
    "Home": "main.py",
    "Simulations": "./pages/simulations.py",
    "About Us": "./pages/about_us.py"
}


# Page Personalization
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")


# Details
st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="font-size: 50px;">
            IT'S NOT JUST AI,<br>IT'S ANOTHER LEVEL,<br>IT'S 
            <span style="font-weight: bold; color: blue; font-style: italic;">GABM</span>
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.subheader("What is GABM?", divider="blue")
    st.write(
        """
        Generative Agent-Based Modeling (GABM) combines generative models and agent-based modeling to create realistic simulations of complex systems.
        By integrating AI-driven agents with a focus on individual behavior, GABM allows for the exploration of interactions and emergent patterns in situations ranging from social networks to ecological models.

        This approach empowers researchers to simulate various scenarios, understand system dynamics, and predict the outcomes of different interventions.
        """)

with col2:
    st.subheader("Why this page?", divider="blue")
    st.write(
        """
        This platform is designed to help researchers and users with minimal programming experience create and experiment with generative agent-based models (GABMs). Using the Concordia framework, this tool makes it easy to build custom agents, explore their attributes, and conduct reliable experiments, all through an accessible and user-friendly interface.
        
        👋 **Hey! Want to know more?** We have stated this concern in [our paper](https://arxiv.org/abs/2411.07038).
        """)

with col3:
    st.subheader("How will we do this?", divider="blue")
    st.write("""
        This platform offers the following key features:

        - **Create Custom Agents:** Design virtual agents with unique attributes and characteristics.
        - **Simulation Design:** Run simulations to observe and analyze agent behaviors and interactions within various scenarios.
        - **Display Agent Information:** Access and review detailed information about each created agent.
        - **Compare Personalities and Ideologies:** Contrast agents with similar or differing political and ideological profiles.
        """)


# Introduction to the Simulations area
st.markdown(
    """
    <h1 style="font-size: 50px; text-align: center; margin-top: 150px;">All set to level up your experiments?</h1>
    """, unsafe_allow_html=True)

st.markdown(
    """
    <style>
        .big-arrow {
            text-align: center;
            font-size: 250px;  /* Very large arrow */
            margin-top: 30px;  /* Add spacing above */
        }
    </style>
    <div class="big-arrow">&#8595;</div> 
    """, unsafe_allow_html=True)

_, _, col1, col2, _, _ = st.columns([1, 1, 1, 1, 1, 1]) 

with col1:
    feature_button = st.button("Simulations", use_container_width=True)
    if feature_button:
        page_file = pages["Simulations"]
        st.switch_page(page_file)

with col2:
    about_us_button = st.button("About Us", use_container_width=True)
    if about_us_button:
        page_file = pages["About Us"]
        st.switch_page(page_file)

st.markdown("<br><br><br>", unsafe_allow_html=True) 
