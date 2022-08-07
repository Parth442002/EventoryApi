from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from .models import Event, MediaModel
from rest_framework.permissions import AllowAny
from .serializers import EventSeriallizer
from .permissions import isCreator
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


class GetEventView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EventSeriallizer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EditEventView(APIView):
    permission_classes = [isCreator]

    def put(self, request, id):
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # Updating the Event Object
        serializer = EventSeriallizer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
