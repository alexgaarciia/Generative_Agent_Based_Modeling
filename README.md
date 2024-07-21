# ConcordiaSims
## Overview
The main goal of this repository is to carry out simulations using generative agent-based models (GABMs). These are computer simultaions used to study interactions between people, things, places and time. The main characteristic is that these are constructed using LLMs so that they act reasonably.

## Framework
In order to carry out these simulations, there are many frameworks, but one that stands out is [Concordia](https://github.com/google-deepmind/concordia), a library for generative social simulation. 

It makes it easy to create and use models where agents act on their own. You can define environments with a special agent called the Game Master (GM), who manages the world where player agents interact. The agents say what they want to do in simple language, and the GM turns their words into actions.

*Concordia requires access to a standard LLM API.*

## Main scenario
We will carry out an experiment related to disinformation, but before getting into details, it might be of high relevance to have present its definition, since it is often confused with misinformation. 

The key difference between misinformation and disinformation is that **misinformation** refers to false or inaccurate information that is unintentionally spread, while **disinformation** refers to false or misleading information that is intentionally spread with the purpose of deceiving or manipulating others.

For this scenario, we will look at different types of people based on their political ideologies and a survey about disinformation, and observe how fake news spreads based on those types.

### Part 1: Definition of premise, subgoals, goal, and context
* Premise: The study of disinformation and its rapid spread poses new challenges beyond the established conventions of traditional media studies. Unlike misinformation, disinformation involves the intentional spread of false or misleading information to deceive or manipulate. Understanding how fake news spreads and evaluating the effectiveness of various strategies to prevent its spread is crucial in today's information landscape.

* Subgoals:
  1. Spread a piece of fake news and observe how it propagates among different types of individuals.
  2. Evaluate the effectiveness of various strategies and tools designed to prevent the spread of fake news in real-time.

* Goal: Introduce a piece of fake news and observe its spread. Identify and assess the effectiveness of different strategies and tools used to prevent the spread of fake news, providing insights into which methods are most successful.

* Context: This is an interdisciplinary research workshop where several participants engage with the topic of disinformation to develop innovative and speculative views on how fake news spreads and assess the effectiveness of various strategies to combat it in real-time.

## Files available in the repository
