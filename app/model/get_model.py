import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
import os
from google.cloud import aiplatform
from dotenv import load_dotenv
from app.model import param

# Load environment variables from .env file
load_dotenv()

# Set the environment variable to point to the service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\User\Downloads\avid-grid-425506-k2-a477e86b604d.json"

try:
    # Initialize the Vertex AI client
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


def acquire_model(user_input):
    try:
        client = multiturn_generate_content(param.SAMPLE_SYSTEM_PROMPT)
        if client is None:
            raise ValueError("Chat client could not be initialized.")

        response = client.send_message(user_input, generation_config=generation_config)
        # Extracting only the text part for serialization
        return response.text if hasattr(response, "text") else str(response)
    except Exception as e:
        print(f"Failed to acquire model: {e}")
        return e
