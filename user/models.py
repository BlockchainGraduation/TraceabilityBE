from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.postgres.fields import ArrayField
import uuid

# Create your models here.


MEMBER = "MEMBER"
FACTORY = "FACTORY"
DISTRIBUTER = "DISTRIBUTER"
RETAILER = "RETAILER"
# DISTRIBUTER = "DISTRIBUTER"

NONE = "NONE"
PENDDING = "PENDDING"
DONE = "DONE"


class CustomUserManager(BaseUserManager):
    def create_superuser(self, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        user = self.create(**extra_fields)
        user.set_password(extra_fields["password"])
        user.save()
        return user


class User(AbstractUser):
    ROLE_CHOICE = [
        (MEMBER, "MEMBER"),
        (FACTORY, "FACTORY"),
        (DISTRIBUTER, "DISTRIBUTER"),
        (RETAILER, "RETAILER"),
    ]
    CONFIRM_CHOICE = [
        (NONE, "NONE"),
        (PENDDING, "PENDDING"),
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
    wallet_private_key = models.CharField(max_length=100, null=True, default=None)
    geographical_address = models.CharField(max_length=100, null=True, default="")
    introduce = models.TextField(default=None, null=True)
    role = models.CharField(choices=ROLE_CHOICE, default=MEMBER, max_length=255)
    otp = models.CharField(max_length=6, null=True, blank=True)
    link = models.JSONField(default=dict)
    account_balance = models.BigIntegerField(default=0)
    confirm_status = models.CharField(
        choices=CONFIRM_CHOICE, default=NONE, max_length=255
    )
    survey = models.JSONField(default=dict)
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    tx_hash = models.CharField(max_length=100, null=True, default=None)
    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.username
