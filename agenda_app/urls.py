from django.urls import path
from .views import GenerateAgendaView, UpdateAgendaView

urlpatterns = [
    path("<uuid:meeting_id>/generate/", GenerateAgendaView.as_view()),
    path("<uuid:meeting_id>/update/", UpdateAgendaView.as_view()),
]
