import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
from google.auth.transport.requests import AuthorizedSession
import os
from google.cloud import aiplatform
from dotenv import load_dotenv
from app.model import param
import base64
import json
from google.auth.transport.requests import AuthorizedSession
from google.auth import default


load_dotenv()

# # Get default credentials
# credentials, _ = default()
#
# try:
#     # Initialize Vertex AI without specifying project ID
#     aiplatform.init(credentials=credentials)
# except Exception as e:
#     print(f"Failed to initialize Vertex AI client: {e}")

try:
    project_id = os.getenv('project')
    aiplatform.init(project=project_id)
except Exception as e:
    print(f"Failed to initialize Vertex AI client: {e}")

generation_config = param.GEN_PARAMETERS
safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_NONE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_NONE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_NONE,
}


def multiturn_generate_content(system_prompt):
    try:
        model = GenerativeModel(param.MODEL, system_instruction=[system_prompt], safety_settings=safety_settings)
        chat = model.start_chat()
        return chat
    except Exception as e:
        print(f"Failed to generate content: {e}")
        return None


def db_query(system_prompt_db):
    try:
        # vertexai.init()
        model = GenerativeModel(param.MODEL, system_instruction=[system_prompt_db], safety_settings=safety_settings)
        chat = model.start_chat()
        return chat
    except Exception as e:
        print(f"Failed to generate content: {e}")
        return None


def explain_content(system_prompt):
    try:
        # vertexai.init()
        model = GenerativeModel(param.MODEL, system_instruction=[system_prompt], safety_settings=safety_settings)
        chat = model.start_chat()
        return chat
    except Exception as e:
        print(f"Failed to generate content: {e}")
        return None
