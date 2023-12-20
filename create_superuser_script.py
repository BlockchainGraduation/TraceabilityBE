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
password = "trung2001"
if not User.objects.filter(username=username).exists():
    user = User.objects.create(
        username,
        "trung@gmail.com",
        password,
        is_admin=True,
        is_staff=True,
        is_active=True,
        role="ADMIN",
    )
    user.set_password(password)
    user.save()
    print(f"Superuser '{username}' đã được tạo thành công.")
else:
    print(f"Superuser '{username}' đã tồn tại.")
