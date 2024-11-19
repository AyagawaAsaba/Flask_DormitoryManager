"""
The flask application package.
"""

from flask import Flask

app = Flask(__name__)

# 导入其他库文件
import DormitoryManager.views
from datetime import timedelta

# 创建Flask项目安全密钥（此密钥跟数据库不相干，仅为创造一个相对安全的加密通道）
app.secret_key = 'Zywz5201314Hst@'
# 设置自动重载模板文件
app.jinja_env.auto_reload = True

app.config['TEMPLATES_AUTO_RELOAD'] = True
# 设置静态文件缓存过期时间
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

