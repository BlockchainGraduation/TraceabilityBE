from django.db import models


# Create your models here.
class ProductImage(models.Model):
    image = models.ImageField(upload_to="traceability/", blank=True, max_length=255)
    product = models.ForeignKey(
        "product.Product", related_name="banner", on_delete=models.CASCADE
    )
    create_at = models.DateTimeField(auto_now_add=True)
