from django.contrib.gis.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import AccountManager


class Account(AbstractBaseUser, PermissionsMixin):
    '''
    CustomAccount Model
    '''
    primary_identifier = models.CharField(unique=True, max_length=200)

    email = models.EmailField(verbose_name="Email",
                              null=True, blank=True, unique=True, max_length=100)
    phone = models.CharField(max_length=50, unique=True, null=True, blank=True)

    username = models.CharField(
        max_length=150, unique=True, null=True, blank=True)
    fullname = models.CharField(max_length=200, blank=True, null=True)

    bio = models.TextField(max_length=300, blank=True, null=True)

    avatar = models.FileField(
        upload_to='userAvatar/', null=True, blank=True)

    character1 = models.IntegerField(default=22, blank=True, null=True)
    character2 = models.IntegerField(default=67, blank=True, null=True)
    character3 = models.IntegerField(default=72, blank=True, null=True)

    longitude = models.FloatField()
    latitude = models.FloatField()
    mpoly = models.MultiPolygonField()

    is_verified = models.BooleanField(default=False)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now_add=True)

    objects = AccountManager()

    USERNAME_FIELD = 'primary_identifier'

    def __str__(self):
        return self.primary_identifier
