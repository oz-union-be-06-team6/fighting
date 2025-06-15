from flask import request, Blueprint, jsonify

from app.models import Question, Image, Choice
from config import db

teto_blp = Blueprint("teto", __name__)

@teto_blp.route("/teto/question", methods=["POST"])
def add_question():
    """
    테토남/테토녀 질문 생성 API
    """
    try:
        data = request.get_json()

        image = Image.query.get(data.get("image_id"))
        if not image:
            return jsonify({"message": "해당 이미지가 존재하지 않습니다."}), 404

        if image.type.value != "sub":
            return jsonify({"message": "이미지 타입은 'sub'이어야 합니다."}), 400

        question = Question(
            title=data.get("title"),
            sqe=data.get("sqe"),
            image_id=data.get("image_id"),
            is_active=data.get("is_active", True),
        )
        db.session.add(question)
        db.session.commit()

        return jsonify({"message": f"질문 '{question.title}' 생성 완료"}), 201

    except KeyError as e:
        return jsonify({"message": f"필수 항목이 누락되었습니다: {str(e)}"}), 400


@teto_blp.route("/teto/questions/<int:sqe>", methods=["GET"])
def fetch_question(sqe):
    """
    특정 sqe에 해당하는 질문과 선택지 조회
    """
    question = Question.query.filter_by(sqe=sqe, is_active=True).first()
    if not question:
        return jsonify({"error": "질문을 찾을 수 없습니다."}), 404

    image = Image.query.get(question.image_id)

    choices = (
        Choice.query.filter_by(question_id=question.id, is_active=True)
        .order_by(Choice.sqe)
        .all()
    )

    return jsonify({
        "title": question.title,
        "image_url": image.url if image else None,
        "choices": [choice.to_dict() for choice in choices],
    })


@teto_blp.route("/teto/questions/count", methods=["GET"])
def total_questions():
    total = Question.query.filter_by(is_active=True).count()
    return jsonify({"count": total})
