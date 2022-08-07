from ast import Return
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from .models import Event, MediaModel, Tags
from rest_framework.permissions import AllowAny
from .serializers import EventSerializer, TagsSerializer
from .permissions import isCreator, TagsPermission
# Create your views here.


class EventListView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        querySet = Event.objects.all()
        serializer = EventSerializer(querySet, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateEventView(APIView):
    def post(self, request):
        data = request.data
        event_media = data["media"]
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
        serializer = EventSerializer(new_event)

        return Response(serializer.data)


class GetEventView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EditEventView(APIView):
    permission_classes = [isCreator, ]

    def put(self, request, id):
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # Updating the Event Object
        serializer = EventSerializer(event, data=request.data)
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


class CurrentUserEventsView(APIView):
    def get(self, request):
        creator = request.user
        Userevents = Event.objects.filter(creator=creator)
        serializer = EventSerializer(Userevents, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class TagsListView(APIView):
    permission_classes = [TagsPermission, ]

    def get(self, request):
        tags = Tags.objects.all()
        serializer = TagsSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        new_tag = Tags.objects.create(
            tag_name=data["tag_name"],
            tag_desc=data["tag_desc"],
            bannerImg=data["bannerImg"],
            posterImg=data["posterImg"]
        )
        new_tag.save()
        serializer = TagsSerializer(new_tag)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagsView(APIView):
    #permission_classes = [TagsPermission, ]

    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        else:
            return False

    def get(self, request, id):
        try:
            tag = Tags.objects.get(id=id)
        except Tags.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TagsSerializer(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)
