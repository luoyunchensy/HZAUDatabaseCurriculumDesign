# app.py
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import CheckConstraint

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:314159265@localhost/youyiku'
db = SQLAlchemy(app)


# 用户表的定义，根据你的实际数据库设计修改
class User(db.Model):
    __tablename__ = 'User'

    UID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Uname = db.Column(db.String(20), nullable=False)
    UPass = db.Column(db.String(20), nullable=False)
    UAdress = db.Column(db.String(255), nullable=False)
    UTele = db.Column(db.String(20), nullable=False)


# 其他表的定义，类似地根据实际设计修改

# ... 上面的代码不变 ...
# app.py
# ... 上面的代码不变 ...

# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 查询数据库，检查用户名是否存在
        user = User.query.filter_by(Uname=username).first()

        if user:
            # 验证密码是否匹配
            if user.UPass == password:
                # 验证成功，可以在这里设置用户登录状态，例如使用 session
                return redirect(url_for('index'))
            else:
                # 密码不匹配，设置错误消息
                error = '密码错误'
        else:
            # 用户名不存在，设置错误消息
            error = '用户名不存在'

    return render_template('login.html', error=error)


# ... 下面的代码不变 ...

# 注册页面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        address = request.form['address']
        telephone = request.form['telephone']

        # 在这里你可以进行用户名和密码的验证，例如检查用户名是否已经存在

        # 将用户信息写入数据库
        new_user = User(Uname=username, UPass=password, UAdress=address, UTele=telephone)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('register.html')


# ... 下面的代码不变 ...


# 定义服装表
class Clothing(db.Model):
    __tablename__ = 'Costume'

    CID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CType = db.Column(db.String(20), nullable=False)
    UPrice = db.Column(db.Numeric(8, 2), nullable=False)
    Material = db.Column(db.String(20), nullable=False)
    Color = db.Column(db.String(20), nullable=False)
    Size = db.Column(db.Enum('S', 'M', 'L', 'XL', 'XXL', '均码'), nullable=False)
    AddDate = db.Column(db.DateTime, nullable=False)
    Sales = db.Column(db.Integer, default=0)
    Status = db.Column(db.String(10), default='库存充足')
    PicPath = db.Column(db.String(255))
    Descrip = db.Column(db.String(255))


# 其他表的定义，类似地根据实际设计修改

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
