from django.urls import path, include
from .views import CreateEventView, EventListView, GetEventView, EditEventView, CurrentUserEventsView, TagsListView

urlpatterns = [

    # Event EndPoints
    path("", EventListView.as_view()),
    path("createEvent/", CreateEventView.as_view()),
    path("<uuid:id>/", GetEventView.as_view()),
    path("edit/<uuid:id>/", EditEventView.as_view()),
    path("currentUserEvents/", CurrentUserEventsView.as_view()),

    # Tags EndPoints
    path("tags/", TagsListView.as_view()),
]
