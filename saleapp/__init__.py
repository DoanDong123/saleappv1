from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
app = Flask(__name__)

app.secret_key = "123asdasd123123sd"

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/saleapp?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)

admin = Admin(app=app, name="Quan Ly Ban Hang", template_mode="bootstrap3")

