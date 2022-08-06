from django.db import transaction
from rest_framework import serializers
from .models import Event, MediaModel


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaModel
        fields = ["id", "media", "date_created"]


class EventSeriallizer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source="creator.primary_identifier")
    media = MediaSerializer(many=True)

    class Meta:
        model = Event
        fields = ["id", "event_name", "creator", "creator_name",
                  "event_info", "private_event", "bannerImg", "posterImg", "media", "location", "longitude", "latitude", "mpoly"]
        extra_kwargs = {"id": {"read_only": True}}
