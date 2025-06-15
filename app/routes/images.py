# images.py

from flask import request
from flask_restx import Namespace, Resource, fields

# Namespace 분리
api = Namespace('Image', description='Image related operations')

# Swagger 모델 정의
image_model = api.model('ImageCreate', {
    'url': fields.String(required=True, description='Image URL'),
    'type': fields.String(required=True, description='Image type (main or sub)', enum=['main', 'sub'])
})

# 이미지 생성 (7-1)
@api.route('/')
class CreateImage(Resource):
    @api.expect(image_model)
    def post(self):
        data = request.get_json()
        # 실제 DB 저장로직은 생략 (여기선 mock response)
        return {'message': 'ID: 5 Image Success Create'}, 200