from user.models import User

username = "admin"
password = "trung@gmail.com"

# Kiểm tra xem superuser đã tồn tại chưa
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, "admin@example.com", password)
    print(f"Superuser '{username}' đã được tạo thành công.")
else:
    print(f"Superuser '{username}' đã tồn tại.")
