import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from .models import Vendor, Order, OrderItem
from .process import process_order_event

@csrf_exempt
def ingest_event(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        required_fields = ['vendor_id', 'order_id', 'items', 'timestamp']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'Missing field: {field}'}, status=400)

        # Validate timestamp
        timestamp = parse_datetime(data['timestamp'])
        if not timestamp:
            return JsonResponse({'error': 'Invalid timestamp format'}, status=400)

        # Validate items
        if not isinstance(data['items'], list) or not data['items']:
            return JsonResponse({'error': 'Items must be a non-empty list'}, status=400)

        for item in data['items']:
            if not all(k in item for k in ['sku', 'qty', 'unit_price']):
                return JsonResponse({'error': 'Each item must contain sku, qty, unit_price'}, status=400)

        # Ensure vendor exists
        vendor, _ = Vendor.objects.get_or_create(vendor_id=data['vendor_id'])

        # Create a minimal Order entry (details computed later)
        order = Order.objects.create(
            vendor=vendor,
            order_id=data['order_id'],
            timestamp=timestamp,
            total_amount=0,  # will be updated later
            high_value=False
        )

        # Save OrderItems
        for item in data['items']:
            OrderItem.objects.create(
                order=order,
                sku=item['sku'],
                qty=item['qty'],
                unit_price=item['unit_price']
            )
        print("queue creation")
        # Queue for async processing
        process_order_event.delay(order.id)

        return JsonResponse({'message': 'Event received and queued'}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)