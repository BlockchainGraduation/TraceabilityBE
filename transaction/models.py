from django.db import models

# from product.models import Product
# from user.models import User
# Create your models here.

PENDDING = "PENDDING"
REJECT = "REJECT"
ACCEPT = "ACCEPT"
DONE = "DONE"


class Transaction(models.Model):
    STATUS_CHOICE = [
        (PENDDING, "PENDDING"),
        (ACCEPT, "ACCEPT"),
        (REJECT, "REJECT"),
        (DONE, "DONE"),
    ]

    create_by = models.ForeignKey("user.User", on_delete=models.PROTECT)
    product_id = models.ForeignKey(
        "product.Product", related_name="transaction_product", on_delete=models.PROTECT
    )
    quantity = models.IntegerField()
    price = models.IntegerField()
    active = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICE, default=PENDDING, max_length=255)
    is_reject = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_id.name
