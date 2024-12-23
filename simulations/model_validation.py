import sys
from pathlib import Path

# Add the path to the "simulations" directory
validation_dir = Path("./simulations")
sys.path.append(str(validation_dir))

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
        if model_name == "codestral-latest":
            model = mistral_model.MistralLanguageModel(api_key=api_key, model_name=model_name)
        else:
            model = gpt_model.GptLanguageModel(api_key=api_key, model_name=model_name)
            
        model.sample_text("How are you?")
        return True 
    
    except Exception as e:
        print(f"Model validation failed: {e}")
        return False 
    