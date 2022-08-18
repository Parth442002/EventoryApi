from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
import uuid

user_model = get_user_model()


class MediaModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    media = models.FileField(upload_to='eventImages/', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)


class Tags(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    tag_name = models.CharField(max_length=100, unique=True)
    tag_desc = models.TextField(max_length=300, blank=True, null=False)
    verified = models.BooleanField(default=False)
    bannerImg = models.ImageField(
        upload_to='tagBanner/', null=True, blank=True)
    posterImg = models.ImageField(
        upload_to='tagPoster/', null=True, blank=True)

    def __str__(self):
        return self.tag_name


class Event(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    event_name = models.CharField(max_length=200, blank=False, null=False)
    creator = models.ForeignKey(user_model, on_delete=models.CASCADE)
    event_info = models.TextField(max_length=400, null=True, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    private_event = models.BooleanField(default=False)

    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    last_date_to_register = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    bannerImg = models.ImageField(
        upload_to='eventBanners/', null=True, blank=True)
    posterImg = models.ImageField(
        upload_to='eventPosters/', null=True, blank=True)
    media = models.ManyToManyField(
        MediaModel, blank=True)

    # Location Based Fields
    location = models.CharField(max_length=300, blank=True, null=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    mpoly = models.MultiPolygonField(null=True, blank=True)

    def __str__(self):
        return f"{self.event_name} by {self.creator}"
