import json


def get_text_answer(text_path: str) -> str:
    with open(text_path, "r", encoding='utf-8') as read_file:
        text_answer = json.load(read_file)
    return text_answer
