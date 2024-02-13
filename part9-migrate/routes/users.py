from flask.views import MethodView
from flask import jsonify, request
from flask_smorest import Blueprint
from marshmallow import Schema, fields
from db import db
from models.users import User

# 스키마 정의
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)

# Flask-Smorest Blueprint 설정
user_blp = Blueprint('users', 'users', url_prefix='/users', description='Operations on users')

@user_blp.route('/')
class UserList(MethodView):
    @user_blp.response(200, UserSchema(many=True))
    def get(self):
        users = User.query.all()
        user_data = [{"id":user.id, "name": user.name, "email": user.email} for user in users]  # Convert to list
        return jsonify(user_data)

    @user_blp.arguments(UserSchema)
    @user_blp.response(201, UserSchema)
    def post(self, new_data):
        print("요청은 오는가?")
        user_data = request.json
        new_user = User(name=user_data['name'], email=user_data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created"}), 201

@user_blp.route('/<int:user_id>')
class UserResource(MethodView):
    @user_blp.response(200, UserSchema)
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return {"name": user.name, 'email': user.email}

    @user_blp.arguments(UserSchema)
    @user_blp.response(200, UserSchema)
    def put(self, new_data, user_id):
        user = User.query.get_or_404(user_id)
        user_data = request.json

        user.name = user_data['name']
        user.email = user_data['email']

        db.session.commit()
        return {"message": "User updated"}

    @user_blp.response(204)
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}