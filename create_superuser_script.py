import os
from django.core.wsgi import get_wsgi_application

# Đặt biến môi trường DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "traceability_be.settings")

# Khởi tạo ứng dụng Django
application = get_wsgi_application()

# Import model User từ ứng dụng auth
from user.models import User

# Kiểm tra xem superuser đã tồn tại chưa
username = "trung"
password = "trug2001"
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, "trung@gmail.com", password)
    print(f"Superuser '{username}' đã được tạo thành công.")
else:
    print(f"Superuser '{username}' đã tồn tại.")
