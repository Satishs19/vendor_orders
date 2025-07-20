from django.urls import path
from .views import query_agent

urlpatterns = [
    path('', query_agent)
]