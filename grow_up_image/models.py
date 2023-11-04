from django.db import models


# Create your models here.
class GrowupImage(models.Model):
    image = models.ImageField(upload_to="traceability/", blank=True)
    product = models.ForeignKey(
        "growup.GrowUp", related_name="growup_banner", on_delete=models.CASCADE
    )
    create_at = models.DateTimeField(auto_now_add=True)
