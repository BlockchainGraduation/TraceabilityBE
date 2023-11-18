from django.db import models


# Create your models here.
class Cart(models.Model):
    create_by = models.ForeignKey(
        "user.User", related_name="carts", on_delete=models.CASCADE
    )
    product_id = models.ForeignKey(
        "product.Product", related_name="product_carts", on_delete=models.CASCADE
    )
    create_at = models.DateTimeField(auto_now_add=True)
