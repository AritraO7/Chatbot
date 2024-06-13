from fastapi import APIRouter, HTTPException, Depends, Request, Response
from pydantic import BaseModel
from app.model.get_model import multiturn_generate_content, param
import base64
from typing import Optional
from fastapi import UploadFile, File
from vertexai.generative_models import Part
from app.service_impl.chat import generation,generation_with_doc
chatbot = APIRouter()
chat_client = multiturn_generate_content(param.SYSTEM_PROMPT_2)


class Prompt(BaseModel):
    user_prompt: str
    document: Optional[str]= None


@chatbot.post("/medical_bot")
async def chat(prompt: Prompt):
    global chat_client
    try:
        if chat_client is None:
            raise HTTPException(status_code=500, detail="Chat client initialization failed")
        response = generation(prompt.user_prompt, chat_client)
        # response = chat_client.send_message(
        #     prompt.user_prompt, generation_config=param.GEN_PARAMETERS
        # )
        return {"response": response.text if hasattr(response, "text") else str(response)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@chatbot.post("/upload_file/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    encoded_contents = base64.b64encode(contents).decode("utf-8")
    return {"filename": file.filename, "base64": encoded_contents}


@chatbot.post("/medical_bot_with_pdf")
async def chat_with_pdf(prompt: Prompt):
    global chat_client
    try:
        if chat_client is None:
            raise HTTPException(status_code=500, detail="Chat client initialization failed")

        context_part = Part.from_data(
            mime_type="application/pdf",
            data=base64.b64decode(prompt.document)
        )
        response = generation_with_doc(context_part, prompt.user_prompt, chat_client)
        # response = chat_client.send_message(
        #     [context_part, prompt.user_prompt], generation_config=param.GEN_PARAMETERS
        # )
        return {"response": response.text if hasattr(response, "text") else str(response)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@chatbot.post("/medical_bot_pdf")
async def chat_with_pdf(prompt, file: UploadFile = File(...)):
    global chat_client
    try:
        if chat_client is None:
            raise HTTPException(status_code=500, detail="Chat client initialization failed")
        contents = await file.read()
        encoded_contents = base64.b64encode(contents).decode("utf-8")
        context_part = Part.from_data(
            mime_type="application/pdf",
            data=base64.b64decode(encoded_contents)
        )
        response = generation_with_doc(context_part, prompt, chat_client)
        return {"response": response.text if hasattr(response, "text") else str(response)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    sample_response = generation(param.SAMPLE_PROMPT)
    print(sample_response.text)
