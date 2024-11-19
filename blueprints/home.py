from flask import Blueprint, render_template, request, redirect, url_for, session, flash
# 引入时间戳
from datetime import datetime

# 把Url的视图函数的前缀
bp = Blueprint('home', __name__, url_prefix="/home")


@bp.route('/dashboard')
def dashboard():
    """Renders the home page."""
    return render_template(
        'pages/dashboard.html',
        title="仪表盘",
        year=datetime.now().year
    )


# 宿舍列表
@bp.route('/home_list')
def home_list():
    """Renders the home page."""
    return render_template(
        'pages/component/table/auto.html',
        title="宿舍列表",
        year=datetime.now().year
    )


# 申请入住
@bp.route('/home_states')
def home_states():
    """Renders the home page."""
    return render_template()


# 申请退房
@bp.route('/home_checkout')
def home_checkout():
    """Renders the home page."""
    return render_template()


# 维修登记
@bp.route('/fix')
def fix():
    """Renders the home page."""
    return render_template()


# 宿舍安全
@bp.route('/security')
def security():
    """Renders the security page."""
    return render_template()


# 学生卫生
@bp.route('/students_healthy')
def students_healthy():
    """Renders the students healthy page."""
    return render_template()


# 宿舍卫生
@bp.route('/rooms_healthy')
def rooms_healthy():
    """Renders the rooms healthy page."""
    return render_template()


# 充值余额
@bp.route('/balance')
def home_stay():
    """Renders the balance page."""
    return render_template()


# 充值电费
@bp.route('/balance_electricity')
def balance_electricity():
    """Renders the balance page."""
    return render_template()


# 充值水费
@bp.route('/balance_water')
def balance_water():
    """Renders the balance page."""
    return render_template()


# 学生签到
@bp.route('/students_signs')
def students_signs():
    """Renders the students sign page."""
    return render_template()


# 学生请假
@bp.route('/students_leave')
def students_sign():
    """Renders the students sign page."""
    return render_template()


# 学生用户
@bp.route('/user_list')
def user_list():
    """Renders the user page."""
    return render_template(
        'pages/user/user/list.html',
        title="学生用户",
        year=datetime.now()
    )


@bp.route('/user_admin')
def user_admin():
    """Renders the user page."""
    return render_template(
        'pages/user/administrators/list.html',
        test='{{#  if(d.check == true){ }}',
        ifs='{{#  } else { }}',
        ends='{{#  } }}',
        admins="{{#  if(d.role == '超级管理员'){ }}"
    )


@bp.route('/user_role')
def user_role_list():
    """Renders the role page."""
    return render_template(
        'pages/user/administrators/role.html',
        test='{{#  if(d.check == true){ }}',
        ifs='{{#  } else { }}',
        ends='{{#  } }}'
    )


@bp.route('/user_message')
def user_message_list():
    """Renders the message page."""
    return render_template(
        'pages/app/message/index.html',
        title="消息中心",
        year=datetime.now()
    )


@bp.route('/setting_web')
def setting_web():
    """Renders the setting page."""
    return render_template(
        'pages/set/system/website.html', title="网站设置", year=datetime.now().year
    )


@bp.route('/setting_mail')
def setting_mail():
    """Renders the setting page."""
    return render_template(
        'pages/set/system/email.html', title="邮件设置"
    )


@bp.route('/setting_user_info')
def setting_user_info():
    """Renders the setting page."""
    return render_template(
        'pages/set/user/info.html', title="基本信息", year=datetime.now().year
    )


@bp.route('/setting_password')
def setting_password():
    """Renders the setting page."""
    return render_template(
        'pages/set/user/password.html', title="修改密码", year=datetime.now().year
    )
