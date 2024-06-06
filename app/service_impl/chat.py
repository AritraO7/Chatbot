from app.model.get_model import acquire_model


def start_chat(chat,user_prompt):
    return chat.send_message(user_prompt)


def generation(user_prompt: str, chat):
    """
    Here the user query is taken and answer with a chatbot
    :return:
    """
    chat = acquire_model()
    response = start_chat(chat, user_prompt)
    return response.text

