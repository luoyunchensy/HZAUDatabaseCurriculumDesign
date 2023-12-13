# app.py
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import Clothing
from models import User
from models import db
from models import ShopCart
from sqlalchemy import CheckConstraint, func

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:314159265@localhost/youyiku'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)


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
                session['username'] = username
                session['user_id'] = user.UID
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


@app.route('/logout')
def logout():
    # 清除用户的会话信息
    session.pop('username', None)
    # 重定向到登录页面或其他页面
    # return redirect(url_for('login'))
    username = session.get('username')
    return redirect(url_for('index'))
    #return render_template('index.html', username=username)


@app.route('/clothing/<int:cid>')
def clothing_detail(cid):
    # 根据衣服的 CID 查询数据库获取衣服的详细信息
    username = session.get('username')
    user_id = session.get('user_id')
    clothing = Clothing.query.get(cid)
    print(username)
    # 渲染详情页模板，将衣服的详细信息传递给模板
    return render_template('clothing_detail.html', username=username, user_id=user_id, clothing=clothing)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    # 从前端获取衣服信息
    data = request.get_json()
    uid = data.get('uid')
    cid = data.get('cid')
    number = data.get('number')

    # 查询购物车中是否已存在该 CID
    existing_cart_item = ShopCart.query.filter_by(UID=uid, CID=cid).first()

    # 插入购物车表的逻辑...
    if existing_cart_item:
        existing_cart_item.number+=number
    else:
        new_cartitem = ShopCart(UID=uid, CID=cid, number=number)
        db.session.add(new_cartitem)

    db.session.commit()

    # 返回一个成功的响应
    return jsonify({'message': 'success'})

@app.route('/')
def index():
    username = session.get('username')
    user_id = session.get('user_id')
    # print(username)
    # print(user_id)
    # clothes = Clothing.query.all()
    clothes = db.session.query(
        Clothing.CName,
        func.max(Clothing.CID).label('CID'),
        func.max(Clothing.UPrice).label('UPrice'),
        func.max(Clothing.PicPath).label('PicPath')
    ).group_by(Clothing.CName).all()
    return render_template('index.html', clothes=clothes, username=username,user_id=user_id)


if __name__ == '__main__':
    app.run(debug=True)
