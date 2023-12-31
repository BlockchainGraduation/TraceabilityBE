from django.db import models
from django.contrib.postgres.fields import ArrayField

# from transaction.models import Transaction
# from user.models import User
# Create your models here.


class Product(models.Model):
    # id=models.UUIDField(primary_key=True)
    create_by = models.ForeignKey(
        "user.User", related_name="product", on_delete=models.PROTECT
    )
    transaction_id = models.ForeignKey(
        "transaction.Transaction", on_delete=models.PROTECT, null=True, default=None
    )
    name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to="traceability/", blank=True)
    description = models.TextField(max_length=255)
    # banner = models.ManyToManyField("image.Image")
    price = models.IntegerField()
    quantity = models.IntegerField()
    product_type = models.CharField(max_length=255)
    # product_status = models.CharField()
    active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tx_hash = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name
