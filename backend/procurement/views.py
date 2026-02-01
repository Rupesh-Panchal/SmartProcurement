from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Vendor
import math

@api_view(['POST'])
def optimize_order(request):
    # Read input from request
    required_length = int(request.data.get('required_length'))
    quantity = int(request.data.get('quantity'))

    RAW_TUBE_LENGTH = 6000  

    pieces_per_tube = RAW_TUBE_LENGTH // required_length
    raw_tubes_required = math.ceil(quantity / pieces_per_tube)

    vendors = Vendor.objects.all()
    best_vendor = None
    lowest_cost = None

    for vendor in vendors:
        total_cost = vendor.price_per_tube * raw_tubes_required

        if lowest_cost is None or total_cost < lowest_cost:
            lowest_cost = total_cost
            best_vendor = vendor

        elif total_cost == lowest_cost:
            if vendor.delivery_days < best_vendor.delivery_days:
                best_vendor = vendor

    return Response({
        "raw_tubes_required": raw_tubes_required,
        "vendor": {
            "name": best_vendor.name,
            "total_cost": lowest_cost,
            "delivery_days": best_vendor.delivery_days
        }
    })
