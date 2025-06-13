from datetime import datetime
from enum import Enum
from zoneinfo import ZoneInfo
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
KST = ZoneInfo("Asia/Seoul")

# 🔹 공통 속성 모델 (id, created_at, updated_at)
class CommonModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tz=KST), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(tz=KST), onupdate=lambda: datetime.now(tz=KST), nullable=False)


# 🔹 ENUM 정의
class AgeStatus(Enum):
    teen = "teen"
    twenty = "twenty"
    thirty = "thirty"
    forty = "forty"
    fifty = "fifty"

class GenderStatus(Enum):
    male = "male"
    female = "female"

class ImageStatus(Enum):
    main = "main"
    sub = "sub"


# 🔹 사용자 정보
class User(CommonModel):
    __tablename__ = "users"
    name = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Enum(AgeStatus), nullable=False)
    gender = db.Column(db.Enum(GenderStatus), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    answers = db.relationship("Answer", backref="user", lazy=True)


# 🔹 이미지 정보 (질문과 연결됨)
class Image(CommonModel):
    __tablename__ = "images"
    url = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum(ImageStatus), nullable=False)

    questions = db.relationship("Question", backref="image", lazy=True)


# 🔹 설문 질문
class Question(CommonModel):
    __tablename__ = "questions"
    image_id = db.Column(db.Integer, db.ForeignKey("images.id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    sqe = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    choices = db.relationship("Choice", backref="question", lazy=True)


# 🔹 선택지 (에겐/테토 점수 포함!)
class Choice(CommonModel):
    __tablename__ = "choices"
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    sqe = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)




# 🔹 사용자의 답변 기록
class Answer(CommonModel):
    __tablename__ = "answers"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    choice_id = db.Column(db.Integer, db.ForeignKey("choices.id"), nullable=False)
