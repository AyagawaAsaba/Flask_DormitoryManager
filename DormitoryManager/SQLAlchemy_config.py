# 导入主文件__init__.py
from DormitoryManager import app
# 导入备用数据库文件
from flask_sqlalchemy import SQLAlchemy

# 配置备用数据库项
HOSTNAME = 'localhost'
PORT = '3306'
USERNAME = 'root'
PASSWORD = 'adminroot'
DATABASE = 'dormitorymanager'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

# 调用备用数据库链接
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
# 动态追踪数据库的修改，不建议开启
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 备用数据库调用
db = SQLAlchemy()

# 示例代码
# with app.app_context():
#     with db.engine.connect() as conn:
#         res = conn.execute("select 1")
#         print(res.fetchone())  # (1,)
