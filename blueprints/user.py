# 导入字串符数据、随机值
import random
import string
# 导入时间模块
from datetime import datetime
# 导入 flask 用到的库
from flask import Blueprint, render_template, request, jsonify, redirect, session, url_for, sessions, flash
# 导入邮箱信息模块
from flask_mail import Message
# 验证模块
from wtforms.validators import ValidationError
# 导入邮箱
from DormitoryManager.Mail_config import mail
# 导入数据库
from DormitoryManager.SQLAlchemy_config import db
# 导入模型
from DormitoryManager.models import EmailCaptchaModel, UserModel
# from blueprints.forms import RegisterForm
from blueprints.forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

# 把Url的视图函数的前缀
bp = Blueprint('user', __name__, url_prefix="/user")


# 登录界面
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # print(request.form)
        return render_template(
            'login.html',
            title="登录 | 学生宿舍系统",
            year=datetime.now().year
        )
    else:
        form = LoginForm(request.form)
        print(request.form)
        # print(form)

        # if form.validate():
        if form:
            # if form.validate_on_submit():

            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            # print(user)

            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect(url_for('dashboard'))

            else:
                flash("邮箱和密码不匹配！")
                return redirect(url_for('user.login', _flash=True))

        else:
            flash("邮箱或密码格式错误！")
            return redirect(url_for('user.login', _flash=True))

    # if request.method == 'POST':
    #     # 获取用户输入的用户名和密码
    #     email = request.form.get('email')
    #     password = request.form.get('password')
    #
    #     # 查询数据库，验证用户名和密码是否匹配
    #     user = User.query.filter_by(email=email, password=password).first()
    #
    #     if user:
    #         # 用户名和密码匹配，登录成功
    #         session['user_id'] = user.id  # 将用户ID存储在会话中
    #         return redirect('/user/dashboard')  # 重定向到用户仪表板或其他页面
    #     else:
    #         # 用户名和密码不匹配，显示错误消息
    #         return render_template('login.html', message='Invalid username or password.')

    # 如果是GET请求，显示登录页面
    # return render_template(
    #     'login.html',
    #     title="登录 | 学生宿舍系统",
    #     year=datetime.now().year
    # )


# 用户注册页面
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        print(request.form)

        return render_template(
            'register.html',
            title="注册 | 学生宿舍系统",
            year=datetime.now().year,
            message='Your application Register Page.')
    else:
        form = RegisterForm(request.form)
        print(request.form)
        # print(form.recaptcha)

        # if form.validate():
        if form:
            try:
                # 调用验证码验证
                form.validate_captcha(form.recaptcha)
                print(form.validate_captcha(form.recaptcha))
                # 调用邮箱验证
                form.validate_email(form.email)
                print(form.validate_email(form.email))

                # 如果验证通过，创建用户并进行其他操作
                username = form.username.data
                email = form.email.data
                password = form.password.data
                # confirm_password = form.confirm_password.data
                # MD5加密     # md(123456)  ==>  "fiberglassFUYEF"
                hash_password = generate_password_hash(password)
                user = UserModel(username=username, email=email, password=hash_password)
                print(user.username, user.email, user.password)
                db.session.add(user)
                db.session.commit()

                flash('注册成功！请登录。', 'success')
                return redirect(url_for('user.login'))
            except ValidationError as e:
                # 处理验证错误
                flash(str(e), 'error')

        return render_template(
            'register.html',
            title="注册 | 学生宿舍系统",
            year=datetime.now().year,
            form=form,
            message='Your application Register Page.'
        )


# 用户注销页面
@bp.route("/logout")
def logout():
    # 清除session中所有的数据
    session.clear()
    return redirect(url_for('qa.index'))


# 忘记密码界面
@bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    return render_template(
        'forget.html',
        title="忘记密码 | 学生宿舍系统",
        year=datetime.now().year,
    )


@bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    return render_template(
        'reset_password.html',
        title="重置密码 | 学生宿舍系统",
        year=datetime.now().year
    )


@bp.route('/reset_email', methods=['GET', 'POST'])
def reset_email():
    return render_template(
        'reset_email.html',
        title="重置邮箱 | 学生宿舍系统",
        year=datetime.now().year
    )


# 邮箱验证码接口
@bp.route('/captcha', methods=['POST'])
def get_captcha():
    name = request.args.get('name')
    email = request.args.get('email')
    my_string = string.ascii_letters + string.digits
    captcha = "".join(random.sample(my_string, 4))
    if email:
        message = Message(
            subject='验证你的 学生宿舍 账号',
            recipients=[email],
            body=f"""
亲爱的{name}!\n 
    非常感谢您的访问，欢迎来到 学生宿舍管理系统，在完成 账号注册 之前，我们需要验证一下您的邮箱哦~\n 
        您的验证码为：{captcha}!\n
    如果在您没有注册的情况下接受到此验证码，请不要管他；并且不要将此验证码告诉他人!\n
最后，感谢您的访问，祝您使用愉快！
            """
        )
        mail.send(message)
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if captcha_model:
            captcha_model.captcha = captcha
            captcha_model.create_time = datetime.now()
            db.session.commit()
        else:
            captcha_model = EmailCaptchaModel(email=email, captcha=captcha)
            db.session.add(captcha_model)
            db.session.commit()
        print("验证码为：" + captcha)
        return jsonify({'code': 200, 'success': True, 'message': "验证码发送成功！" + "您的验证码为：" + captcha})
    else:
        return jsonify({'code': 400, 'success': False, 'message': "请先输入邮箱后再获取验证码！"})


# memcached/redis/db
# 邮箱测试
@bp.route('/mail')
def send_mail():
    message = Message(
        subject='Test',
        recipients=['hst1368@outlook.com'],
        body=f"【测试邮件】"
    )
    mail.send(message)
    return "测试发送成功"
