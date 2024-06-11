from fastapi import APIRouter, HTTPException, Depends, Request
from app.service_impl.chat import generation
from pydantic import BaseModel
from app.model import param


chatbot = APIRouter()


class Prompt(BaseModel):
    user_prompt: str


@chatbot.post("/medical_bot")
async def chat(prompt: Prompt):
    try:
        response = generation(prompt.user_prompt)
        if isinstance(response, Exception):
            raise HTTPException(status_code=500, detail=str(response))
        return  str(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    sample_response = generation(param.SAMPLE_PROMPT)
    print(sample_response.text)
