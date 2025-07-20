import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vendor_orders.settings')

app = Celery('vendor_orders')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()