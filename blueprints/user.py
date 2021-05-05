from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# define the blueprint
user = Blueprint(name="user", import_name=__name__)

from app import db, ma

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(65))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "password")

#Initialize Schema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

#Get All users
@user.route("", methods=["GET"])
def get_users():
    all_users = User.query.all()

    result = users_schema.dump(all_users)
    return jsonify(result)

#Get user
@user.route("<id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

#Add user
@user.route("", methods=["POST"])
def add_user():
    name = request.json["name"]
    email = request.json["email"]
    password = request.json["password"]
    new_user = User(name, email, password)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


#Update user
@user.route("<id>", methods = ["PUT"])
def update_user(id):
    user = User.query.get(id)

    name = request.json["name"]
    email = request.json["email"]
    password = request.json["password"]

    user.name = name
    user.email = email
    user.password = password

    db.session.commit()
    return user_schema.jsonify(user)

@user.route("<id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)

db.create_all()
