from django.urls import path, include
from .views import CreateEventView, AllEventsView, GetEventView, EditEventView

urlpatterns = [
    path("", AllEventsView.as_view()),
    path("createEvent/", CreateEventView.as_view()),
    path("<uuid:id>/", GetEventView.as_view()),
    path("edit/<uuid:id>/", EditEventView.as_view()),
]
