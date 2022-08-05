from django.db import transaction
from rest_framework import serializers
from .valueCheck import emailValidator, phoneValidator, usernameValidator
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Account
from dj_rest_auth.registration.serializers import RegisterSerializer


class CustomRegisterSerializer(RegisterSerializer):
    primary_identifier = serializers.CharField(max_length=100)
    username = None
    email = None
    phone = None

    # Define transaction.atomic to rollback the save operation in case of error

    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        primary_identifier = self.data.get("primary_identifier")
        user.primary_identifier = primary_identifier

        if emailValidator(primary_identifier) == True:
            user.email = primary_identifier
            user.username = None
            user.phone = None
        if phoneValidator(primary_identifier) == True:
            user.phone = primary_identifier
            user.username = None
            user.email = None
        if usernameValidator(primary_identifier) == True:
            user.username = primary_identifier
            user.email = None
            user.phone = None
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['primary_identifier'] = user.primary_identifier
        token["id"] = user.id

        return token


class AccountDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        #fields = ['id', 'username', 'email', 'phone', 'is_verified']
        extra_kwargs = {"password": {"write_only": True}}
