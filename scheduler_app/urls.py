from django.urls import path
from .views import (
    MeetingListCreateView,
    MeetingDetailView,
    TriggerView,
    ScheduleMeetingView
)

urlpatterns = [
    path("meetings/", MeetingListCreateView.as_view(), name="meeting-list"),
    path("meetings/<uuid:pk>/", MeetingDetailView.as_view(), name="meeting-detail"),
    
    path("trigger/", TriggerView.as_view()),
    path("schedule/", ScheduleMeetingView.as_view()),
]
