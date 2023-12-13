# app/models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# 定义服装表
class Clothing(db.Model):
    __tablename__ = 'Costume'

    CID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CName = db.Column(db.String(20), nullable=False)
    CType = db.Column(db.String(20), nullable=False)
    CTag = db.Column(db.String(20), nullable=False)
    UPrice = db.Column(db.Numeric(8, 2), nullable=False)
    Material = db.Column(db.String(20), nullable=False)
    Color = db.Column(db.String(20), nullable=False)
    Size = db.Column(db.Enum('S', 'M', 'L', 'XL', 'XXL', '均码'), nullable=False)
    AddDate = db.Column(db.DateTime, nullable=False)
    Sales = db.Column(db.Integer, default=0)
    Status = db.Column(db.String(10), default='库存充足')
    PicPath = db.Column(db.String(255))
    Descrip = db.Column(db.String(255))



class User(db.Model):
    __tablename__ = 'User'

    UID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Uname = db.Column(db.String(20), nullable=False)
    UPass = db.Column(db.String(20), nullable=False)
    UAdress = db.Column(db.String(255), nullable=False)
    UTele = db.Column(db.String(20), nullable=False)


class ShopCart(db.Model):
    __tablename__ = 'ShopCart'

    CartID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UID = db.Column(db.Integer, nullable=False)
    CID = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    # # 添加外键关联
    # user = db.relationship('User', backref='shopcarts')
    # costume = db.relationship('Clothing', backref='shopcarts')