# app/models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # 其他用户信息的字段...


# 在工厂函数中初始化数据库
# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # 配置数据库连接等...
    app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri'

    db.init_app(app)

    # 注册蓝图等其他操作...

    return app
