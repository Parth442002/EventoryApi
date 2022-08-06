from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event, MediaModel
from rest_framework.permissions import AllowAny
from .serializers import EventSeriallizer
# Create your views here.


class AllEventsView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        querySet = Event.objects.all()
        serializer = EventSeriallizer(querySet, many=True)
        return Response(serializer.data)


class CreateEventView(APIView):

    def post(self, request):
        data = request.data
        event_media = []
        new_event = Event.objects.create(
            event_name=data["event_name"],
            creator=request.user,
            event_info=data["event_info"],
            private_event=data["private_event"],
            bannerImg=data["bannerImg"],
            posterImg=data["posterImg"],
            location=data["location"],
            longitude=data["longitude"],
            latitude=data["latitude"],
            mpoly=data["mpoly"],

        )
        new_event.save()

        for media in event_media:
            media_obj = MediaModel.objects.get(module_name=media["media"])
            new_event.media.add(media_obj)

        new_event.save()
        serializer = EventSeriallizer(new_event)

        return Response(serializer.data)
