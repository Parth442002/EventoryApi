from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from authentication.models import Account
from .models import FriendRequest
from .serializers import ListFriendRequestSerializers, FriendListSerializer
# Create your views here.


class AllIncommingFriendRequestsView(APIView):
    """
    View to get all the incomming Friend Request for the current user
    """
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        to_account = request.user
        friendrequests = FriendRequest.objects.filter(
            to_account=to_account, is_active=True
        )
        serializer = ListFriendRequestSerializers(friendrequests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllOutGoingFriendRequestsView(APIView):
    """
    View to get all the friend request that the current signed in user has sent out
    """
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        from_account = request.user
        friendrequests = FriendRequest.objects.filter(
            from_account=from_account
        )
        serializer = ListFriendRequestSerializers(friendrequests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SendFriendRequestView(APIView):
    """
    View to send a friend Request to another account.
    """

    def post(self, request):
        from_account = request.user
        to_account = request.data["userID"]
        friend_request, created = FriendRequest.objects.get_or_create(
            from_account=from_account, to_account=to_account,
        )
        if created:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_200_OK)


class AcceptFriendRequestView(APIView):
    """
    View to accept friend request
    """

    def post(self, request):
        requestID = request.data["requestID"]
        friend_request = FriendRequest.objects.get(id=requestID)
        if friend_request.to_user == request.user:
            friend_request.to_user.friends.add(friend_request.from_user)
            # Adding friends for both of the accounts
            friend_request.from_user.friends.add(friend_request.to_user)
            friend_request.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DeclineFriendRequestView(APIView):
    """
    Api View to decline an upcomming FriendRequest
    """

    def post(self, request):
        requestID = request.data["requestID"]
        friend_request = FriendRequest.objects.get(id=requestID)
        if request.to_user == request.user:
            friend_request.is_active = False
            friend_request.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class AllFriendsView(APIView):
    """
    Get all the friends of the signed in user.
    """

    def get(self, request):
        user = Account.objects.get(id=request.user.id)
        if user.exists():
            friends = user.friends.all()
            serializer = FriendListSerializer(friends)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
