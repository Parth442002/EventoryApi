from django.urls import path, include
from .views import AllEventsView, CreateEventView

urlpatterns = [
    path("allEvents/", AllEventsView.as_view()),
    path("createEvent/", CreateEventView.as_view()),
]
