from fastapi import APIRouter
from fastapi import HTTPException
from app.service_impl.chat import generation
from pydantic import BaseModel

chatbot = APIRouter()


class Prompt(BaseModel):
    user_prompt: str


@chatbot.post("/medical_bot")
def chat(prompt: Prompt):
    try:
        response = generation(prompt.user_prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


