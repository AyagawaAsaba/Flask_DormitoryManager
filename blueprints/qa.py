from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime

# 把Url的视图函数的前缀
bp = Blueprint('qa', __name__, url_prefix="/")


@bp.route('/')
def index():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='主页 | 学生宿舍管理',
        year=datetime.now().year,
    )
