from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('', home, name='home'),  # <-- add this line
    path('admin/', admin.site.urls),
    path('api/scheduler/', include('scheduler_app.urls')),
    path('api/agendas/', include('agenda_app.urls')),
    path('api/transcription/', include('transcription_app.urls')),
    path('api/tasks/', include('tasks_app.urls')),
    path('api/notifications/', include('notifications_app.urls')),
    path('api/reports/', include('reports_app.urls')),
    path('api/auth/', include('auth_app.urls')),
]
