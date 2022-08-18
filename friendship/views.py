from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from authentication.models import Account
from .models import FriendRequest
from .serializers import ListFriendRequestSerializers, SingleFriendSerializer
# Create your views here.


class AllFriendsView(APIView):
    """
    Get all the friends of the signed in user.
    """

    def get(self, request):
        user = Account.objects.get(id=request.user.id)
        friends = user.friends.all()
        print(friends)
        serializer = SingleFriendSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        userID = request.data["userID"]
        to_account = Account.objects.get(id=userID)
        friend_request, created = FriendRequest.objects.get_or_create(
            from_account=from_account, to_account=to_account,
        )
        if created:
            return Response(friend_request.id, status=status.HTTP_201_CREATED)
        else:
            return Response(friend_request.id, status=status.HTTP_200_OK)


class AcceptFriendRequestView(APIView):
    """
    View to accept friend request
    """

    def post(self, request):
        requestID = request.data["requestID"]
        friend_request = FriendRequest.objects.get(id=requestID)
        if friend_request.to_account == request.user:
            friend_request.to_account.friends.add(friend_request.from_account)
            # Adding friends for both of the accounts
            friend_request.from_account.friends.add(friend_request.to_account)
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


class RemoveFriendView(APIView):
    """
    View to remove a friend
    """

    def post(self, request):
        current_user = request.user
        userID = request.data["userID"]
        friend = current_user.friends.get(id=userID)
        if friend:
            current_user.friends.remove(friend)
            return Response("Its workinggg")


class BlockAccountView(APIView):
    """
    Api View to Block a certain Account
    """

    def post(self, request):
        current_user = request.user
        userID = request.data["useriD"]
        if userID:
            current_user.block_account(userID)
            return Response(f"{userID} just got blocked", status=status.HTTP_200_OK)
        else:
            return Response(f"Could not Block {userID}", status=status.HTTP_400_BAD_REQUEST)


class UnBlockAccountView(APIView):
    """
    Api View to UnBlock a certain Account
    """

    def post(self, request):
        current_user = request.user
        userID = request.data["useriD"]
        if userID:
            current_user.unblock_account(userID)
            return Response(f"{userID} just got unblocked", status=status.HTTP_200_OK)
        else:
            return Response(f"Could not UnBlock {userID}", status=status.HTTP_400_BAD_REQUEST)
