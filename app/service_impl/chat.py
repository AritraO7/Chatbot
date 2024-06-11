from app.model.get_model import acquire_model
from app.model import param


def generation(user_prompt: str):
    try:
        response = acquire_model(user_prompt)
        if response is None or isinstance(response, Exception):
            raise ValueError("Failed to acquire response from model")
        # Assuming response.text is the attribute you want to return.
        return response
    except Exception as e:
        return e


if __name__ == '__main__':
    sample_response = acquire_model(param.SAMPLE_PROMPT)
    print(sample_response.text)
