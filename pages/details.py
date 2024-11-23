import streamlit as st

# Dictionary mapping page names to functions
pages = {
    "Home": "main.py",
    "Simulations": "./pages/simulations.py",
    "About Us": "./pages/about_us.py"
}


# Background styling
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 88% 102%,#3E3EDE, #BEE8DF, #60CAE8, #99B5D5)
    }
    </style>
    """, unsafe_allow_html=True)


# Details
st.markdown(
    """
    <h1 style="font-size: 60px;">IT'S NOT JUST AI,<br>IT'S ANOTHER LEVEL,<br>IT'S <span style="font-weight: bold; color: blue; font-style: italic;">GABM</span></h1>
    """, unsafe_allow_html=True)

st.markdown(
    """
    <p style="width: 600px; height: 300px; ">
        Generative Agent-Based Modeling (GABM) combines generative models and agent-based modeling to 
        create realistic simulations of complex systems. By integrating AI-driven agents with a focus on individual behavior, 
        GABM allows for the exploration of interactions and emergent patterns in situations ranging from social networks 
        to ecological models. This approach empowers researchers to simulate various scenarios, understand system dynamics, 
        and predict the outcomes of different interventions.
    </p>
    """, unsafe_allow_html=True)


# Why this page?
st.markdown(
    """
    <h1 style="font-size: 60px; margin-left: auto; margin-right: 0; text-align: right; margin-top: -80px;">
        <span style="font-style: italic; color: blue;">Why</span> This Page?
    </h1>
    """, unsafe_allow_html=True)

st.markdown(
    """
    <p style="width: 600px; height: 300px; margin-left: auto; margin-right: 50px; text-align: right">
        This platform is designed to help researchers and users with minimal programming experience create and experiment with
        generative agent-based models (GABMs). Leveraging the Concordia framework, this tool makes it easy to build custom agents,
        explore their attributes, and conduct reliable experiments, all through an accessible and user-friendly interface.
        <br><br>
        👋 Hey! Want to know more? We have stated this concern in our paper: <a href="https://arxiv.org/abs/2411.07038" target="_blank">Designing Reliable Experiments with Generative Agent-Based Modeling: A Comprehensive Guide Using Concordia by Google DeepMind</a>
    </p>
    """, unsafe_allow_html=True)


# How?
st.markdown(
    """
    <h1 style="font-size: 60px;">
        <span style="font-style: italic; color: blue;">How</span> Will We Do This?
    </h1>
    """, unsafe_allow_html=True)

st.markdown(
    """
    <div style="width: 600px; height: auto; text-align: left;">
        <p>This platform offers the following key features:</p>
        <ul>
            <li><strong>Create Custom Agents:</strong> Design virtual agents with unique attributes and characteristics.</li>
            <li><strong>Simulation Design:</strong> Run simulations to observe and analyze agent behaviors and interactions within various scenarios.</li>
            <li><strong>Display Agent Information:</strong> Access and review detailed information about each created agent.</li>
            <li><strong>Compare Personalities and Ideologies:</strong> Contrast agents with similar or differing political and ideological profiles.</li>
        </ul>
    </div>
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

# Introduction to the Simulations area
st.markdown(
    """
    <h1 style="font-size: 50px; text-align: center; margin-top: -100px;">All set to level up your experiments?</h1>
    """, unsafe_allow_html=True
)


# Create a centered row of buttons with reduced space
_, _, col1, col2, col3, _, _ = st.columns([1, 1, 1, 1, 1, 1, 1])  # equal column widths for center alignment

with col1:
    home_button = st.button("Home", use_container_width=True)  # Ensure the button takes full width of the column
    if home_button:
        page_file = pages["Home"]
        st.switch_page(page_file)

with col2:
    feature_button = st.button("Simulations", use_container_width=True)
    if feature_button:
        page_file = pages["Simulations"]
        st.switch_page(page_file)

with col3:
    about_us_button = st.button("About Us", use_container_width=True)
    if about_us_button:
        page_file = pages["About Us"]
        st.switch_page(page_file)

# Add line breaks after the buttons
st.markdown("<br><br><br>", unsafe_allow_html=True)
