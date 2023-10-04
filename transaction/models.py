from django.db import models
# from product.models import Product
# from user.models import User
# Create your models here.

class Transaction(models.Model):
    create_by=models.ForeignKey('user.User',on_delete=models.PROTECT)
    product_id=models.ForeignKey('product.Product',on_delete=models.PROTECT)
    quantity=models.IntegerField(default=0)
    price=models.IntegerField()
    status=models.CharField()
    create_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product_id.name