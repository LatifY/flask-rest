from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#Initialize app
app = Flask(__name__)
#basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'# + os.path.join(basedir, 'db.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app) #Initialize Database
ma = Marshmallow(app) #Initialize Marshmallow

#Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(300), nullable=True)
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

#Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'quantity')


#Initialize Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


#Create a Product
@app.route("/product", methods=["POST"])
def add_product():
    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    quantity = request.json["quantity"]
    new_product = Product(name,description,price,quantity)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

#Get All Products
@app.route("/product", methods=["GET"])
def get_products():
    all_products = Product.query.all()

    result = products_schema.dump(all_products)
    return jsonify(result)

#Get Product
@app.route("/product/<id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)

    return product_schema.jsonify(product)

#Update Product
@app.route("/product/<id>", methods = ["PUT"])
def update_product(id):
    product = Product.query.get(id)

    name = request.json["name"]
    description = request.json["description"]
    price = request.json["price"]
    quantity = request.json["quantity"]

    product.name = name
    product.description = description
    product.price = price
    product.quantity = quantity

    db.session.commit()

    return product_schema.jsonify(product)

@app.route("/product/<id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)


#Run Server
if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()
