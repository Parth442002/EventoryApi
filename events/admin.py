from django.contrib import admin
from .models import Event, MediaModel, Tags
# MediaModel
# Register your models here.

admin.site.register(Event)
admin.site.register(MediaModel)
admin.site.register(Tags)
