from fastapi import FastAPI, HTTPException, Query, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from app.routers.chatbot import chatbot
from app.routers.auth import token
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(token, prefix="/auth", tags=["auth"])
app.include_router(chatbot, prefix="/generation", tags=["playground"])


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=True)




