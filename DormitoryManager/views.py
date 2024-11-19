"""
Routes and views for the flask application.
"""

# 导入时间模块
from datetime import datetime
# 导入Flask模板功能，后续会被合并
from flask import render_template, request, redirect, url_for, session, flash, g, send_from_directory
# 导入绑定模块
from flask_migrate import Migrate
from sqlalchemy.exc import NoResultFound
# 主文件为 __init__.py
from DormitoryManager import app
# 导入Flask数据库    __init__作为头文件，可以临时引用数据库位置，不过为了代码简洁多样性，谷被隔离开来
from DormitoryManager.SQLAlchemy_config import db  # 备用数据库
from DormitoryManager.MySQL_config import mysql  # 主数据库（目前）
from DormitoryManager.Mail_config import mail  # 邮箱功能
# 导入蓝图
from blueprints import qa_bp, user_bp, home_bp
from DormitoryManager.models import UserModel
# 导入模型
# from DormitoryManager.models import EmailCaptchaModel
# 导入Flask配置文件
import DormitoryManager.config
import os

# 引用Flask配置文件
app.config.from_object(DormitoryManager.config)
# 初始化数据库功能
db.init_app(app)
# 绑定蓝图
app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)
app.register_blueprint(home_bp)
# 初始化邮箱功能
mail.init_app(app)
# 初始化绑定
migrate = Migrate(app, db)


# 定义备用数据库用户表
# class User(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = db.Column(db.String(100), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)

# 创建宿舍表
class Dormitory(db.Model):
    __tablename__ = 'dormitory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    # 关联
    students = db.relationship('Student', back_populates='dormitory', lazy=True)


# 创建学生数据表
class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)  # UID 同时作为 学生学号
    name = db.Column(db.String(100), nullable=False)  # 姓名
    email = db.Column(db.String(100), unique=True, nullable=False)  # 邮箱
    phone = db.Column(db.String(100), unique=True, nullable=False)  # 电话号码
    classroom = db.Column(db.String(100), unique=True, nullable=False)  # 学生班级
    balance = db.Column(db.Float, default=0, nullable=False)  # 余额
    header = db.Column(db.LargeBinary, nullable=False)  # 头像
    year = db.Column(db.Integer, nullable=False)  # 学生入学年份
    dormitory_id = db.Column(db.Integer, db.ForeignKey('dormitory.id'), nullable=False)  # 宿舍UID
    # 关联
    dormitory = db.relationship('Dormitory', back_populates='students')
    courses = db.relationship('Course')
    classrooms = db.relationship('Classroom', back_populates='student',
                                 primaryjoin="Student.id == Classroom.student_id")


# 创建房间表表
class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dormitory_id = db.Column(db.Integer, db.ForeignKey('dormitory.id'), nullable=False)


# 创建楼层表
class Floor(db.Model):
    __tablename__ = 'floor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dormitory_id = db.Column(db.Integer, db.ForeignKey('dormitory.id'), nullable=False)


# 创建班级
class Classroom(db.Model):
    __tablename__ = 'classroom'
    id = db.Column(db.Integer, primary_key=True)  # 班级ID
    room_number = db.Column(db.String(255), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('dormitory.id'), nullable=False)  # 班级的？？？
    # 创建课程关联表
    courses = db.relationship('Course', back_populates='classroom', primaryjoin="Classroom.id == Course.classroom_id")
    student = db.relationship('Student', back_populates='classrooms')


# 创建课程表
class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(255), nullable=False)
    classroom_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    # 关联
    student = db.relationship('Student', back_populates='courses')
    classroom = db.relationship('Classroom', back_populates='courses')


# 将所有的表同步到备用数据库中
with app.app_context():
    db.create_all()


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image')


@app.before_request
def before_request():
    user_id = session.get("user_id")
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # 给g绑定一个叫做user的变量，他的值是user这个变量
            # setattr(g,"user",user)
            g.user = UserModel.query.get_or_404(user_id)
        except NoResultFound:
            # 找不到用户时的异常处理，你可以根据需要进行适当的处理
            g.user = None
            # 或者你也可以记录日志等
            app.logger.error(f"User with ID {user_id} not found.")


# 请求来了 -> before_request -> 视图函数 -> 视图函数中返回模板 -> context_processor


@app.context_processor
def context_processor():
    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}


# 主页面，为防止出现引用错误，故增加根目录、home目录 和 index目录
# @app.route('/')
@app.route('/index')
def index():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='主页 | 学生宿舍管理',
        year=datetime.now().year,
    )


# 忘记密码页面
@app.route('/forget', methods=['GET', 'POST'])
def forget():
    if request.method == 'POST':
        email = request.form['email']
        cur = mysql.cursor()
        sql = "DELETE FROM pythonflask.users WHERE email=%s AND password"
        cur.execute(sql, email)
        flash("已为您的邮箱发送新密码，请查看登录后进行更改密码")
        return redirect(url_for('login'))
    return render_template(
        'forget.html',
        title="忘记密码 | 学生宿舍系统",
        year=datetime.now().year,
        message='Your application Forget Password Page.'
    )


# 联系页面
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template(
        'contact.html',
        title="联系我们 | 学生宿舍管理系统",
        year=datetime.now().year
    )


# 画廊页面
@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    return render_template(
        'gallery.html',
        title="宿舍预览 | 学生宿舍管理系统",
        year=datetime.now().year
    )


# 单一图景页面
@app.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    return render_template(
        'portfolio.html',
        title="某宿舍预览 | 学生宿舍管理系统",
        year=datetime.now().year
    )


# ？此页面暂未支配
@app.route('/portfolio-single', methods=['GET', 'POST'])
def portfolio_single():
    return render_template(
        'portfolio-single.html',
        title="某处预览 | 学生宿舍管理系统",
        year=datetime.now().year
    )


# 主页服务帮助页面
@app.route('/services', methods=['GET', 'POST'])
def services():
    return render_template(
        'services.html',
        title="宿舍服务 | 学生宿舍管理系统",
        year=datetime.now().year
    )


# 关于页面
@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template(
        'about.html',
        title="关于 | 学生宿舍管理系统",
        year=datetime.now().year
    )


# 后台界面
@app.route('/dashboard')
def dashboard():
    return render_template(
        'dashboard.html',
        title="仪表盘 | 学生宿舍管理系统",
        year=datetime.now().year,
        message='Your'
    )


# 错误界面（异常处理404）
@app.errorhandler(404)
def not_found(e):
    return render_template(
        "404.html",
        title="哎呀，找不到页面了"
    )

# @app.route('/dormitory/<int:dormitory_id>')
# def dormitory_detail(dormitory_id):
#     dormitory = Dormitory.query.get(dormitory_id)
#     students = Student.query.filter_by(dormitory_id=dormitory_id).all()
#     return render_template('dormitory_detail.html', dormitory=dormitory, students=students)
#
#
# @app.route('/student/<int:student_id>')
# def student_detail(student_id):
#     student = Student.query.get(student_id)
#     return render_template('student_detail.html', student=student)
#
#
# @app.route('/recharge/<int:student_id>', methods=['POST'])
# def recharge(student_id):
#     if request.method == 'POST':
#         amount = float(request.form['amount'])
#         student = Student.query.get(student_id)
#         student.balance += amount
#         db.session.commit()
#     return redirect(url_for('student_detail', student_id=student_id))


# 测试数据集——用户添加
# @app.route('/user/add', methods=['GET', 'POST'])
# def add_user():
#     # 1. 创建User类对象
#     user1 = User(username='user1', email='<EMAIL>', password='<PASSWORD>')
#     # user2 = User(username='user2', email='<EMAIL>', password='<PASSWORD>')
#     # user3 = User(username='user3', email='<EMAIL>', password='<PASSWORD>')
#     # 2. 将User类的对象添加到数据库会话中
#     db.session.add(user1)
#     # db.session.add([user2, user3])
#     # 3. 使用commit() 方法从会话中提交到数据库
#     db.session.commit()
#     return 'redirect(url_for(''))'


# 测试数据集——查询用户ni
# @app.route('/user/query')
# def query_user():
#     # 1. Get查找：根据主键查找，只能查找一条数据
#     # Select username, password from user where id=1
#     # user = User.query.get(1)
#     # print(f"{user.id} | {user.username} | {user.email} | {user.password}")
#     # 2. Filter_by查找
#     users = User.query.filter_by(email='<EMAIL>').all()
#     print(f"{len(users)} | {users}")
#     for user in users:
#         print(user.username)
#     return '数据查询成功'


# 测试数据集——修改更新数据
# @app.route('/user/update', methods=['GET', 'POST'])
# def update_user():
#     user = User.query.filter_by(email='<EMAIL>').first()
#     user.password = '12345678'
#     db.session.commit()
#     return '更新修改数据成功'


# 测试数据集——删除用户数据
# @app.route('/user/delete', methods=['GET', 'POST'])
# def delete_user():
#     # 1. Get查找：根据主键查找，只能查找一条数据
#     user = User.query.get(1)
#     # 2. 将 User 类的对象添加到数据库会话中
#     db.session.delete(user)
#     # 3. 使用 commit() 方法提交到会话中
#     db.session.commit()
#     return '删除用户数据成功'
