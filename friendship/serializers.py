from rest_framework import serializers
from .models import FriendRequest
from authentication.models import Account


class ListFriendRequestSerializers(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ["id", "from_account", "to_account", "is_active", "send_date"]


class SingleFriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', "primary_identifier")
