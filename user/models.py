from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.postgres.fields import ArrayField
import uuid

# Create your models here.


MEMBER = "MEMBER"
FISHERMEN = "FISHERMEN"
SEEDLING = "SEEDLING"
FACTORY = "FACTORY"
DISTRIBUTER = "DISTRIBUTER"

NONE = "NONE"
PENDING = "PENDING"
DONE = "DONE"


class User(AbstractUser):
    ROLE_CHOICE = [
        (MEMBER, "MEMBER"),
        (FISHERMEN, "FISHERMEN"),
        (SEEDLING, "SEEDLING"),
        (FACTORY, "FACTORY"),
        (DISTRIBUTER, "DISTRIBUTER"),
    ]
    CONFIRM_CHOICE = [
        (NONE, "NONE"),
        (PENDING, "PENDING"),
        (DONE, "DONE"),
    ]
    first_name = (None,)
    last_name = None

    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )
    fullname = models.TextField(default=None, null=True)
    avatar = models.ImageField(upload_to="traceability/", blank=True)
    phone = models.TextField(null=True, default=None)
    wallet_address = models.CharField(max_length=100, null=True, default=None)
    geographical_address = models.CharField(max_length=100, null=True, default="")
    introduce = models.TextField(default=None, null=True)
    role = models.CharField(choices=ROLE_CHOICE, default=MEMBER)
    otp = models.CharField(max_length=6, null=True, blank=True)
    link = models.JSONField(default=dict)
    confirm_status = models.CharField(choices=CONFIRM_CHOICE, default=NONE)
    survey = models.JSONField(default=dict)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username
