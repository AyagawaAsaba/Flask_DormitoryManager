from datetime import timedelta

# 模板文件自动重载
TEMPLATES_AUTO_RELOAD = True
# 设置静态文件缓存过期时间
SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
# 是否启用JSON的ASCII编码
