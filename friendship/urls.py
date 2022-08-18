from django.urls import path
from .views import AcceptFriendRequestView, AllFriendsView, AllIncommingFriendRequestsView, AllOutGoingFriendRequestsView, DeclineFriendRequestView, SendFriendRequestView

urlpatterns = [

    # All Friends
    path("", AllFriendsView.as_view()),

    # ALL Requests
    path("incomingRequests/", AllIncommingFriendRequestsView.as_view()),
    path("outgoingRequests/", AllOutGoingFriendRequestsView.as_view()),

    # Request Actions
    path("sendRequest/", SendFriendRequestView.as_view()),
    path("acceptRequest/", AcceptFriendRequestView.as_view()),
    path("declineRequest/", DeclineFriendRequestView.as_view()),

]
