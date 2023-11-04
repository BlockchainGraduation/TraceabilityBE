from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class RoleChoice(models.TextChoices):
    MEMBER = "MEMBER", "MEMBER"
    FARMER = "FARMER", "FARMER"
    SEED_COMPANY = "SEED_COMPANY", "SEED_COMPANY"
    FACTORY = "FACTORY", "FACTORY"
    DISTRIBUTER = "DISTRIBUTER", "DISTRIBUTER"


class User(AbstractUser):
    first_name = None
    last_name = None

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullname = models.TextField(default=None, null=True)
    avatar = models.ImageField(upload_to="traceability/", blank=True)
    phone = models.TextField(unique=True)
    wallet_address = models.CharField(max_length=100, null=True, default=None)
    geographical_address = models.CharField(max_length=100, null=True, default="")
    role = models.CharField(choices=RoleChoice.choices, default=RoleChoice.MEMBER)
    otp = models.CharField(max_length=6, null=True, blank=True)
    link = models.JSONField(default=dict)

    def __str__(self) -> str:
        return self.username
