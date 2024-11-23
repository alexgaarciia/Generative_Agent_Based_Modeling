import streamlit as st

# Dictionary mapping page names to functions
pages = {
    "Home": "main.py",
    "Key Features": "./pages/features.py",
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


# Introduction to the Simulations area

# Create n columns to place the buttons side by side
col1, col2, col3 = st.columns(3)

with col1:
    home_button = st.button("Home")
    if home_button:
        # Switch to the selected page
        page_file = pages["Home"]
        st.switch_page(page_file)

with col2:
    feature_button = st.button("Key Features")
    if feature_button:
        # Switch to the "Key Features" page
        page_file = pages["Key Features"]
        st.switch_page(page_file)

with col3:
    about_us_button = st.button("About Us")
    if about_us_button:
        # Switch to the "About Us" page
        page_file = pages["About Us"]
        st.switch_page(page_file)