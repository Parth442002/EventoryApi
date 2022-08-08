from django.db import transaction
from rest_framework import serializers
from .valueCheck import emailValidator, phoneValidator, usernameValidator
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Account, FriendRequest
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
        token["id"] = str(user.id)

        return token


class AccountDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ["id", "primary_identifier", "email", "phone", "username",         "fullname", "bio", "avatar", "character1", "character2", "character3",
                  "longitude", "latitude", "mpoly", "dark_theme", "is_verified",
                  "is_superuser",
                  "is_staff",
                  "is_active",
                  "date_joined",
                  "last_login",
                  "groups",
                  "user_permissions",
                  "friends"
                  ]
        #fields = ['id', 'username', 'email', 'phone', 'is_verified']
        extra_kwargs = {"password": {"write_only": True}}
