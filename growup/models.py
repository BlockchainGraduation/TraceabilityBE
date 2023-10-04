from django.db import models
from django.contrib.postgres.fields import ArrayField
from product.models import Product
# Create your models here.

class GrowUp(models.Model):
    product_id=models.ForeignKey(Product,on_delete=models.PROTECT)
    title=models.CharField()
    description=models.CharField()
    image=ArrayField(models.ImageField(upload_to=''))
    def __str__(self):
        return self.title