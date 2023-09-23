from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class User(AbstractUser):
    choices_role=[('FM','Fammer'),('SC','SeedCompany'),('FT','Factory'),('DT','Distributor')]
    avatar=models.ImageField(upload_to="uploads/%Y/%m/%d/",)
    phone=models.TextField(unique=True)
    wallet_address=models.CharField(unique=True,max_length=100, default='')
    geographical_address=models.CharField(unique=True,max_length=100, default='')
    role=models.CharField(choices=choices_role)