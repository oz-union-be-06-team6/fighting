from flask import Blueprint, request, jsonify
from app.models import db, User, AgeStatus, GenderStatus
from sqlalchemy.exc import SQLAlchemyError

user_blp = Blueprint("users", __name__, url_prefix="/users")

# 회원가입 API (POST /signup)
@user_blp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    required_fields = ["name", "email", "age", "gender"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field}은(는) 필수 필드입니다."}), 400

    # ✅ 이메일 중복 체크
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "이미 존재하는 이메일입니다."}), 400

    try:
        # 문자열 → Enum 변환
        age_enum = AgeStatus[data["age"]]
        gender_enum = GenderStatus[data["gender"]]

        new_user = User(
            name=data["name"],
            email=data["email"],
            age=age_enum,
            gender=gender_enum
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": f"{new_user.name}님 회원가입을 축하합니다!",
            "user_id": new_user.id
        }), 201

    except KeyError:
        return jsonify({"error": "age 또는 gender 값이 유효하지 않아요."}), 400

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "데이터베이스 오류: " + str(e)}), 500