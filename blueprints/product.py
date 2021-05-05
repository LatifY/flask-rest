from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# define the blueprint
product = Blueprint(name="product", import_name=__name__)

from blueprints.category import Category
from app import db, ma



#Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoryId = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(300), nullable=True)
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def __init__(self, categoryId, name, description, price, quantity):
        self.name = name
        self.categoryId = categoryId
        self.description = description
        self.price = price
        self.quantity = quantity

#Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'categoryId', 'name','description', 'price', 'quantity')


#Initialize Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

#Get All Products
@product.route("", methods=["GET"])
def get_products():
    all_products = Product.query.all()

    result = products_schema.dump(all_products)
    return jsonify(result)

#Get Product
@product.route("<id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)

    return product_schema.jsonify(product)

#Add Product
@product.route("", methods=["POST"])
def add_product():
    name = request.json["name"]
    categoryId = request.json["categoryId"]
    description = request.json["description"]
    price = request.json["price"]
    quantity = request.json["quantity"]

    check = Category.query.filter_by(id = categoryId).first() != None
    if(check):
        new_product = Product(name, categoryId, description,price,quantity)
        db.session.add(new_product)
        db.session.commit()
        return product_schema.jsonify(new_product)
    else:
        return "Invalid Category ID"



#Update Product
@product.route("<id>", methods = ["PUT"])
def update_product(id):
    product = Product.query.get(id)

    name = request.json["name"]
    categoryId = request.json["categoryId"]
    description = request.json["description"]
    price = request.json["price"]
    quantity = request.json["quantity"]

    check = Category.query.filter_by(id = categoryId).first() != None
    if(check):
        product.name = name
        product.categoryId = categoryId
        product.description = description
        product.price = price
        product.quantity = quantity

        db.session.commit()

        return product_schema.jsonify(product)
    else:
        return "Invalid Category ID"

@product.route("<id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)
db.create_all()
