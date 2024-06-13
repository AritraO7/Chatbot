import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
import os
from google.cloud import aiplatform
from dotenv import load_dotenv
from app.model import param
import base64


load_dotenv()


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\User\Downloads\avid-grid-425506-k2-a477e86b604d.json"

try:
    aiplatform.init()
except Exception as e:
    print(f"Failed to initialize Vertex AI client: {e}")

generation_config = param.GEN_PARAMETERS


def multiturn_generate_content(system_prompt):
    try:
        vertexai.init(project="avid-grid-425506-k2", location="us-central1")
        model = GenerativeModel(param.MODEL, system_instruction=[system_prompt])
        chat = model.start_chat()
        return chat
    except Exception as e:
        print(f"Failed to generate content: {e}")
        return None
