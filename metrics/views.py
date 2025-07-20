import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date, timedelta
from django.db.models.functions import TruncDate
from django.db.models import Count
from events.models import Vendor, Order
from .models import VendorMetrics


@csrf_exempt
def vendor_metrics(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    vendor_id = request.GET.get('vendor_id')
    if not vendor_id:
        return JsonResponse({'error': 'Missing vendor_id parameter'}, status=400)
    vendor_obj = Vendor.objects.get(vendor_id=vendor_id)
    
    seven_days_ago = date.today() - timedelta(days=7)

    recent_orders = (
    Order.objects
    .filter(vendor=vendor_obj, timestamp__date__gte=seven_days_ago)
    .annotate(day=TruncDate('timestamp'))
    .values('day')
    .annotate(count=Count('id'))
    )

    volume_dict = {str(entry['day']): entry['count'] for entry in recent_orders}

    try:
        vendor = Vendor.objects.get(vendor_id=vendor_id)
        metrics = VendorMetrics.objects.get(vendor=vendor)

        # Volume in the last 7 days
        seven_days_ago = date.today() - timedelta(days=7)
        recent_orders = (
            Order.objects
            .filter(vendor=vendor, timestamp__date__gte=seven_days_ago)
            .annotate(day=TruncDate('timestamp'))
            .values('day')
            .annotate(count=Count('id'))
        )

        volume_dict = {str(entry['day']): entry['count'] for entry in recent_orders}

        response = {
            'vendor_id': vendor.vendor_id,
            'total_orders': metrics.total_orders,
            'total_revenue': float(metrics.total_revenue),
            'high_value_orders': metrics.high_value_orders,
            'last_7_days_volume': volume_dict
        }

        return JsonResponse(response, status=200)

    except Vendor.DoesNotExist:
        return JsonResponse({'error': f'No such vendor: {vendor_id}'}, status=404)
    except VendorMetrics.DoesNotExist:
        return JsonResponse({'error': 'Metrics not found for this vendor'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

