from django.db import models


# Create your models here.
COMMENT_PRODUCT = "COMMENT_PRODUCT"
NONE = "NONE"


class Notification(models.Model):
    ROLE_CHOICE = [(COMMENT_PRODUCT, "COMMENT_PRODUCT"), (NONE, "NONE")]
    product_id = models.ForeignKey(
        "product.Product", related_name="product_notification", on_delete=models.PROTECT
    )
    notification_type = models.CharField(
        choices=ROLE_CHOICE, default="NONE", max_length=255
    )
    active = models.BooleanField(default=False)
    create_by = models.ForeignKey(
        "user.User", related_name="user_notification", on_delete=models.PROTECT
    )
    create_at = models.DateTimeField(auto_now_add=True)
