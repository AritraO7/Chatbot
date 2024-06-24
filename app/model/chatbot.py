import json
from fastapi import APIRouter, HTTPException, Depends, Request, Response
from pydantic import BaseModel
from app.model.get_model import multiturn_generate_content,db_query, explain_content, param
import base64
from typing import Optional
from fastapi import UploadFile, File
from vertexai.generative_models import Part
import re, os
from app.service_impl.chat import generation,generation_with_doc,database_query,database_explain
from app.bigquery.bigquery import connect_bq
import google.cloud.logging
import logging

chatbot = APIRouter()
client = google.cloud.logging.Client(project=os.getenv('project'))
log_name = "Caresaathi"
logger = client.logger(log_name)



chat_client = multiturn_generate_content(param.SYSTEM_PROMPT_2)
db_client = db_query(param.SYSTEM_PROMPT_DB)
exp_client = explain_content(param.SYSTEM_PROMPT_EXP)


class Prompt(BaseModel):
    user_prompt: str
    document: Optional[str] = None


def extract_sql_from_markdown(markdown_response):
    # Regular expression to match the SQL code block within triple backticks
    pattern = r'```sql\n(.*?)\n```'
    match = re.search(pattern, markdown_response, re.DOTALL)

    if match:
        # Extracted SQL query
        sql_query = match.group(1)
        return sql_query
    else:
        raise ValueError("No SQL query found in the markdown response")


@chatbot.post("/medical_bot")
async def chat(prompt: Prompt):
    global chat_client
    try:
        if chat_client is None:
            text = f"Chat client initialization failed."
            logger.log_text(text)
            print("Logged: {}".format(text))
            raise HTTPException(status_code=500, detail="Chat client initialization failed")
        response = generation(prompt.user_prompt, chat_client)
        text = f"Medical query successfully generated."
        logger.log_text(text)
        print("Logged: {}".format(text))
        return {"response": response.text if hasattr(response, "text") else str(response)}

    except Exception as e:
        text = f"Following exception occurred : {str(e)}"
        logger.log_text(text)
        print("Logged: {}".format(text))
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
            text = f"Chat client initialization failed."
            logger.log_text(text)
            print("Logged: {}".format(text))
            raise HTTPException(status_code=500, detail="Chat client initialization failed")

        context_part = Part.from_data(
            mime_type="application/pdf",
            data=base64.b64decode(prompt.document)
        )
        response = generation_with_doc(context_part, prompt.user_prompt, chat_client)
        text = f"Medical query with document successfully generated."
        logger.log_text(text)
        print("Logged: {}".format(text))
        return {"response": response.text if hasattr(response, "text") else str(response)}

    except Exception as e:
        text = f"Exception occurred as {str(e)}"
        logger.log_text(text)
        print("Logged: {}".format(text))
        raise HTTPException(status_code=500, detail=str(e))


@chatbot.post("/medical_bot_pdf")
async def chat_with_pdf(prompt, file: UploadFile = File(...)):
    global chat_client
    try:
        if chat_client is None:
            text = f"Chat client initialization failed."
            logger.log_text(text)
            print("Logged: {}".format(text))
            raise HTTPException(status_code=500, detail="Chat client initialization failed")
        contents = await file.read()
        encoded_contents = base64.b64encode(contents).decode("utf-8")
        context_part = Part.from_data(
            mime_type="application/pdf",
            data=base64.b64decode(encoded_contents)
        )
        response = generation_with_doc(context_part, prompt, chat_client)
        text = f"Medical query with document successfully generated."
        logger.log_text(text)
        print("Logged: {}".format(text))
        return {"response": response.text if hasattr(response, "text") else str(response)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@chatbot.post("/database_query")
async def chat(prompt: Prompt):
    global db_client, exp_client
    try:
        if db_client is None:
            raise HTTPException(status_code=500, detail="Chat client initialization failed")
        response = database_query(prompt.user_prompt, db_client)
        sql_q = extract_sql_from_markdown(response.text)
        # Replace \n with actual newlines
        sql_query = sql_q.replace('\n', '\n')
        query = response.text
        connect_bq(sql_q)
        # res = connect_bq(sql_q)
        # data = [dict(zip(res.schema.names, row)) for row in res]
        # json_data = json.dumps(data)
        # response = database_explain(exp_client, query, json_data)
        return {"response": sql_q if hasattr(response, "text") else str(response)}

    except Exception as e:
        text = f"Exception occurred as {str(e)}"
        logger.log_text(text)
        print("Logged: {}".format(text))
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    sample_response = generation(param.SAMPLE_PROMPT, chat_client)
    print(sample_response.text)
