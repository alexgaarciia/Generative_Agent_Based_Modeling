# ConcordiaSims
## Overview
The main goal of this repository is to carry out simulations using generative agent-based models (GABMs). These are computer simultaions used to study interactions between people, things, places and time. The main characteristic is that these are constructed using LLMs so that they act reasonably.

## Framework
In order to carry out these simulations, there are many frameworks, but one that stands out is [Concordia](https://github.com/google-deepmind/concordia), a library for generative social simulation. 

It makes it easy to create and use models where agents act on their own. You can define environments with a special agent called the Game Master (GM), who manages the world where player agents interact. The agents say what they want to do in simple language, and the GM turns their words into actions.

*Concordia requires access to a standard LLM API.*
