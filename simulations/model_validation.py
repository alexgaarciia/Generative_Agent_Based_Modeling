"""
This module provides a function to validate the connection to a language model using a given API key and model name.
It verifies that the language model is accessible by attempting to generate a sample response.
"""

import sys
from pathlib import Path

# -----------------------------------------------------------------------------
# Extend Python's module search path to include the "simulations" directory.
# This allows modules within the "simulations" package to be imported.
# -----------------------------------------------------------------------------
validation_dir = Path("./simulations")
sys.path.append(str(validation_dir))

# -----------------------------------------------------------------------------
# Import language model modules from the 'concordia' subpackage.
# Depending on the model name provided, one of these will be used to create
# a language model instance.
# -----------------------------------------------------------------------------
from concordia.language_model import gpt_model
from concordia.language_model import mistral_model

def validate_model(api_key, model_name):
    """
    Validates the connection to the language model using the provided API key and model name.
    
    Parameters:
        api_key (str): The API key for accessing the model.
        model_name (str): The name of the model to be used.
    
    Returns:
        bool: True if the model connection is successful, False otherwise.
    """
    try:
        # Instantiate the appropriate language model based on the model name
        if model_name == "codestral-latest":
            model = mistral_model.MistralLanguageModel(api_key=api_key, model_name=model_name)
            _ = model._client.models.list()
        else:
            model = gpt_model.GptLanguageModel(api_key=api_key, model_name=model_name)
            _ = model._client.models.list() 
        
        return True
    
    except Exception as e:
        # Print the exception message to indicate why validation failed
        print(f"Model validation failed: {repr(e)}")
        return False 
    