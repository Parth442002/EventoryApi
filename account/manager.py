from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, primary_identifier, password=None, **extra_fields):
        if primary_identifier:
            user = self.model(
                primary_identifier=primary_identifier,
                ** extra_fields)

            user.set_password(password)
            user.save(using=self._db)
            return user

            # User Creation INSTANCE

    def create_user(self, primary_identifier, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_verified', True)
        return self._create_user(primary_identifier, password, **extra_fields)

    def create_superuser(self, primary_identifier, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(primary_identifier, password, **extra_fields)
