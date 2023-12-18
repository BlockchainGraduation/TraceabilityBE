from django.db import models


# Create your models here.
class DetailDescription(models.Model):
    product_id = models.ForeignKey(
        "product.Product", related_name="detail_decriptions", on_delete=models.PROTECT
    )
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to="traceability/", blank=True)
