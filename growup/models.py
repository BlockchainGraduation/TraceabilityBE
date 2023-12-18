from django.db import models
from django.contrib.postgres.fields import ArrayField
from product.models import Product

# Create your models here.


class GrowUp(models.Model):
    product_id = models.ForeignKey(
        Product, related_name="growup", on_delete=models.PROTECT
    )
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.title
