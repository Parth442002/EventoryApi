from os import stat
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status, permissions
import environ
import pyotp

from twilio.rest import Client
from .serializers import MyTokenObtainPairSerializer, AccountDetailsSerializer
from .permissions import isVerified
from .models import Account, FriendRequest
from .helpers import sendVerificationMail, sendVerificationSMS

from django.contrib.auth import get_user_model
user_model = get_user_model()

env = environ.Env()


class AccountLoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class AccountLogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            rtoken = request.data["refresh_token"]
            refresh_token = RefreshToken(rtoken)

            atoken = request.data["access_token"]
            access_token = AccessToken(atoken)

            refresh_token.blacklist()
            access_token.blacklist()

            return Response(
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AccountDetailsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = AccountDetailsSerializer(request.user)
        return Response(serializer.data)


class OtpVerifyAccountView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    Createdotp = pyotp.TOTP('base32secret3232', digits=4).now()

    def get(self, request):
        if request.user.primary_identifier == request.user.email:
            response = sendVerificationMail(
                request.user.email, self.Createdotp)
            return Response({
                "message": "Otp Sent Successfully",
                "identifier": request.user.email,
                "data": response
            })
        if request.user.primary_identifier == request.user.phone:
            response = sendVerificationSMS(request.user.phone, self.Createdotp)
            return Response({
                "message": "Otp Sent Successfully",
                "identifier": request.user.phone,
                "data": response
            })

    def post(self, request):
        userInputOtp = request.data['otp']
        if int(userInputOtp) == int(self.Createdotp):
            # Getting the Current Users intance
            current_user = user_model.objects.get(
                primary_identifier=request.user)
            # Updating the Verified Field of currentuser
            current_user.is_verified = True
            current_user.save()
            return Response({"status": True, "message": "Otp Verified Successfully", })
        else:
            return Response({"status": False, "message": "You Entered the Wrong Otp."})


class CheckIsVerifiedView(APIView):
    permission_classes = (isVerified,)

    def get(self, request):
        return Response(True)

    def post(self, request):
        return Response(True)


class SendFriendRequestView(APIView):
    permission_classes = [isVerified, ]

    def get(self, request, userId):
        from_user = request.user
        try:
            to_user = user_model.objects.get(id=userId)
        except user_model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        friend_request, created = FriendRequest.objects.get_or_create(
            from_user=from_user,
            to_user=to_user
        )
        if created:
            return Response(
                {"data": "Friend Request Sent"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"data": "Friend Request was already Sent."},
            status=status.HTTP_200_OK
        )


class AcceptFriendRequestView(APIView):
    def get(self, request, requestID):
        friend_request = FriendRequest.objects.get(id=requestID)
        if friend_request.to_user == request.user:
            friend_request.to_user.friends.add(friend_request.from_user)
            friend_request.from_user.friends.add(friend_request.to_user)
            friend_request.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_200_OK)
