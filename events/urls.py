from django.urls import path
from .views import ingest_event

urlpatterns = [
    path('', ingest_event),
]