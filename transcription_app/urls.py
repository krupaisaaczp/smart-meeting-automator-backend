from django.urls import path
from .views import UploadAudioView, TranscriptStatusView, GetSummaryView
from tasks_app.views import TaskListView as GetTasksView



urlpatterns = [
    path("<uuid:meeting_id>/upload/", UploadAudioView.as_view()),
    path("status/<uuid:transcript_id>/", TranscriptStatusView.as_view()),
    path("<uuid:meeting_id>/summary/", GetSummaryView.as_view()),
    path("<uuid:meeting_id>/tasks/", GetTasksView.as_view()),

]

