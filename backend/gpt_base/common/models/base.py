# from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from gpt_base.common.models.managers import CustomUserManager

class DateTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True

class CustomBaseUserModel(AbstractBaseUser, PermissionsMixin, DateTimeModel):
    email = models.EmailField(max_length=255, unique=True)
    date_joined = models.DateTimeField(('date joined'), default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    class Meta:
        abstract = True

class MaterBaseModel(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    delete_flag = models.BooleanField(default=False)

    class Meta:
        abstract = True
