import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GPAXF.settings')
# 其中daily_fresh 是你的项目名
django.setup()
from django.contrib.auth.hashers import make_password, check_password

password = "12345"
print("password",password)
password_end1 = make_password(password, None, 'pbkdf2_sha256')
print("password",password_end1)
password_end2 = make_password(password, None, 'pbkdf2_sha256')
print(password_end1==password_end2) # 如果第二个参数是None,同样的密码，每次返回都不一样
# 第二个参数，给定参数，每次返回就会相同 slat
print(check_password(password, password_end1))
print(check_password(password, password_end2))
print(check_password("12345", password_end1))