from django.db import models

class Vendor(models.Model):
    vendor_id = models.CharField(max_length=20, unique=True)

class Order(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=20, unique=True)
    timestamp = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    high_value = models.BooleanField(default=False)
    anomalous = models.BooleanField(default=False)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    sku = models.CharField(max_length=30)
    qty = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)