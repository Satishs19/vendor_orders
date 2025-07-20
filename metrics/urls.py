from django.urls import path
from .views import vendor_metrics

urlpatterns = [
    path('', vendor_metrics, name='vendor_metrics'),
]
