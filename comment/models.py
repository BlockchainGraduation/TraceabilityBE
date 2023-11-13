from django.db import models
from product.models import Product
from user.models import User


# Create your models here.
class GrowUp(models.Model):
    product_id = models.ForeignKey(
        Product, related_name="comments", on_delete=models.PROTECT
    )
    user_id = models.ForeignKey(
        User, related_name="product_comment", on_delete=models.PROTECT
    )
    description = models.CharField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
