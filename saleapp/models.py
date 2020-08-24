from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship, backref
from saleapp import db
import datetime, enum
from flask_admin.contrib.sqla import ModelView

class Category(db.Model):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    products = relationship('Product', backref="category", lazy=True)

    def __str__(self):
        return self.name


class Product(db.Model):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, default=0)
    image = Column(String(255), nullable=True)
    create_date = Column(DateTime, default=datetime.datetime.utcnow())
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    creator_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    receipt_detail = relationship('ReceiptDetail', backref='product', lazy=True)

    def __str__(self):
        return self.name

class UserRole(enum.Enum):
    ADMIN = 1
    USER = 2

class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    products = relationship(Product, backref='user', lazy=True)


class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow())
    updated_date = Column(DateTime, default=datetime.datetime.utcnow())
    receiptdetail = relationship('ReceiptDetail', backref='receipt', lazy=True)

class ReceiptDetail(db.Model):
    product_id = Column(Integer, ForeignKey(Product.id), primary_key=True)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), primary_key=True)
    quantity = Column(Integer, default=0)
    unit_price = Column(Integer, default=0)

if __name__ == "__main__":
    db.create_all()
