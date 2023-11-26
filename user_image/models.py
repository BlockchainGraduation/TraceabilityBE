from django.db import models


# Create your models here.
class UserImage(models.Model):
    image = models.ImageField(upload_to="traceability/", blank=True, max_length=255)
    user = models.ForeignKey(
        "user.User", related_name="user_banner", on_delete=models.CASCADE
    )
    create_at = models.DateTimeField(auto_now_add=True)
