from django.db import models
from growup.models import GrowUp


# Create your models here.
class GrowupImage(models.Model):
    image = models.ImageField(upload_to="traceability/", blank=True)
    growup_id = models.ForeignKey(
        GrowUp, related_name="growup_images", on_delete=models.CASCADE
    )
    create_at = models.DateTimeField(auto_now_add=True)
