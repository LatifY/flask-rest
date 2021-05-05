from flask import Flask, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import sys



#Initialize app
app = Flask(__name__)

#Database
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app) #Initialize Database
ma = Marshmallow(app) #Initialize Marshmallow


from blueprints.product import product
from blueprints.category import category

# register blueprints
app.register_blueprint(product, url_prefix="/api/product")
app.register_blueprint(category, url_prefix="/api/category")

if __name__ == "__main__":
    app.run(debug=True)