from django.db import models
from events.models import Vendor

class VendorMetrics(models.Model):
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE)
    total_orders = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    high_value_orders = models.IntegerField(default=0)