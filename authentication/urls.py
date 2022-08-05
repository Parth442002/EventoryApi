from django.urls import path, include
from .views import AccountLoginView, AccountLogoutView, AccountDetailsView, BasicView, OtpVerifyAccountView
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    path('login/', AccountLoginView.as_view()),
    path('logout/', AccountLogoutView.as_view()),
    path('userDetail/', AccountDetailsView.as_view()),
    path('', BasicView.as_view()),
    path('verifyOtp/', OtpVerifyAccountView.as_view()),
    path('verifyToken/', TokenVerifyView.as_view()),
]
