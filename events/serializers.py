from django.db import transaction
from rest_framework import serializers
from .models import Event, MediaModel, Tags


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaModel
        fields = ["id", "media", "date_created"]


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source="creator.primary_identifier")
    media = MediaSerializer(many=True)
    tags = TagsSerializer(many=True)

    class Meta:
        model = Event
        fields = ["id", "event_name", "creator", "creator_name",
                  "event_info", "tags", "private_event", "start_time", "end_time", "last_date_to_register", "date_created", "bannerImg", "posterImg", "media", "location", "longitude", "latitude", "mpoly"]
        extra_kwargs = {"id": {"read_only": True}}
