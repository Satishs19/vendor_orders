from celery import shared_task
from events.models import Order, OrderItem
from metrics.models import VendorMetrics 
from django.db.models import Sum, F

@shared_task
def process_order_event(order_id):
    try:
        order = Order.objects.get(id=order_id)
        items = OrderItem.objects.filter(order=order)

        # Compute total_amount
        total = sum(item.qty * float(item.unit_price) for item in items)
        order.total_amount = total
        order.high_value = total > 500
        order.save()

        # Update vendor metrics
        metrics, _ = VendorMetrics.objects.get_or_create(vendor=order.vendor)
        metrics.total_orders += 1
        metrics.total_revenue += total
        if order.high_value:
            metrics.high_value_orders += 1
        metrics.save()

    except Exception as e:
        print(f"[ERROR] Failed to process order {order_id}: {str(e)}")