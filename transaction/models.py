from django.db import models

# from product.models import Product
# from user.models import User
# Create your models here.


class Transaction(models.Model):
    create_by = models.ForeignKey("user.User", on_delete=models.PROTECT)
    product_id = models.ForeignKey(
        "product.Product", related_name="transaction_product", on_delete=models.PROTECT
    )
    quantity = models.IntegerField()
    price = models.IntegerField()
    active = models.BooleanField(default=False)
    is_reject = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_id.name
