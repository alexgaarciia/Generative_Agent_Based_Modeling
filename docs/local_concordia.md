## How to use Concordia with a local LLM?
Using Concordia with a local LLM could be useful when testing simple functionalities. Here is an explanation on how to do so:

1. Clone this repository in your computer.
2. Install [LM Studio](https://lmstudio.ai/). It is a desktop app for developing and experimenting with LLMs on your computer.
3. Download a model. Please consider RAM and disk space requirements.
4. Once the model is downloaded, it is time to start a local HTTP server that mimics select OpenAI API endpoints. Select the model you want to use, and make sure you **do not change the server port**. Some modifications had to be done to a component of the library that deals with language models. These modifications were done to connect to the specific server http://localhost:1234/v1.
  <p align = "center">
   <img src="https://github.com/alexgaarciia/ConcordiaSims/blob/main/images/local_server.png" width=900>
  </p>
  
5. Open **locally** a notebook available in the repository.
6. When reaching the section about the language model initialization, just change the variable **GPT_MODEL_NAME** to the model you selected.
  <p align = "center">
     <img src="https://github.com/alexgaarciia/ConcordiaSims/blob/main/images/lm_initialization.png" width=900>
  </p>
  
7. Run the notebook.
