import base64
from vertexai.generative_models import Part
from app.model.get_model import multiturn_generate_content, param


def generation(user_prompt: str, client):
    try:
        response = client.send_message(user_prompt,
                                       generation_config=param.GEN_PARAMETERS)

        if response is None or isinstance(response, Exception):
            raise ValueError("Failed")
        return response
    except Exception as e:
        return e


def generation_with_doc(context, user_prompt: str, client):
    try:
        response = client.send_message(
            [context, user_prompt], generation_config=param.GEN_PARAMETERS
        )
        if response is None or isinstance(response, Exception):
            raise ValueError("Failed")
        return response
    except Exception as e:
        return e


if __name__ == '__main__':
    chat_client = multiturn_generate_content(param.SAMPLE_SYSTEM_PROMPT)
    sample_response = generation(param.SAMPLE_PROMPT,chat_client)
    print(sample_response.text)
