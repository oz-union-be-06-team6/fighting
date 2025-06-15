# choices.py

# 질문 ID에 따라 선택지를 정의
question_choices = {
    1: ["예", "아니오"],
    2: ["예", "아니오"],
    3: ["예", "아니오"],
    4: ["예", "아니오"],
    5: ["예", "아니오"],
    6: ["예", "아니오"],
    7: ["예", "아니오"],
    8: ["예", "아니오"],
    9: ["예", "아니오"],
    10: ["예", "아니오"],

}

def get_choices(question_id):
    """
    특정 질문 ID에 해당하는 선택지를 반환합니다.
    없으면 None 반환.
    """
    return question_choices.get(question_id)