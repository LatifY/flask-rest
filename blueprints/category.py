from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# define the blueprint
category = Blueprint(name="category", import_name=__name__)

from app import db, ma

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name

class CategorySchema(ma.Schema):
    class Meta:
        fields = ("id", "name")

#Initialize Schema
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

#Get All categorys
@category.route("", methods=["GET"])
def get_categories():
    all_categories = Category.query.all()

    result = categories_schema.dump(all_categories)
    return jsonify(result)

#Get category
@category.route("<id>", methods=["GET"])
def get_category(id):
    category = Category.query.get(id)

    return category_schema.jsonify(category)

#Add category
@category.route("", methods=["POST"])
def add_category():
    name = request.json["name"]
    new_category = Category(name)

    db.session.add(new_category)
    db.session.commit()

    return category_schema.jsonify(new_category)


#Update category
@category.route("<id>", methods = ["PUT"])
def update_category(id):
    category = Category.query.get(id)

    name = request.json["name"]

    category.name = name

    db.session.commit()

    return category_schema.jsonify(category)

@category.route("<id>", methods=["DELETE"])
def delete_category(id):
    category = Category.query.get(id)
    db.session.delete(category)
    db.session.commit()

    return category_schema.jsonify(category)

db.create_all()
