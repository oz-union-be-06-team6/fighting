# answers.py

import json
import os

ANSWERS_FILE = "answers.json"

def load_answers():
    if not os.path.exists(ANSWERS_FILE):
        return []
    with open(ANSWERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_answers(answers):
    with open(ANSWERS_FILE, "w", encoding="utf-8") as f:
        json.dump(answers, f, ensure_ascii=False, indent=2)

def store_answer(user_id, question_id, answer):
    answers = load_answers()
    response = {
        "user_id": user_id,
        "question_id": question_id,
        "answer": answer
    }
    answers.append(response)
    save_answers(answers)

def get_user_answers(user_id):
    answers = load_answers()
    return [a for a in answers if a["user_id"] == user_id]
