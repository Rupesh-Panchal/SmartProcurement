from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor
import math

@api_view(['POST'])
def optimize_order(request):
    # 1. Validate input
    required_length = request.data.get('required_length')
    quantity = request.data.get('quantity')

    if required_length is None or quantity is None:
        return Response(
            {"error": "required_length and quantity are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        required_length = int(required_length)
        quantity = int(quantity)
    except ValueError:
        return Response(
            {"error": "required_length and quantity must be numbers"},
            status=status.HTTP_400_BAD_REQUEST
        )

    RAW_TUBE_LENGTH = 6000

    # 2. Prevent invalid calculation
    pieces_per_tube = RAW_TUBE_LENGTH // required_length
    if pieces_per_tube == 0:
        return Response(
            {"error": "required_length must be less than 6000"},
            status=status.HTTP_400_BAD_REQUEST
        )

    raw_tubes_required = math.ceil(quantity / pieces_per_tube)

    # 3. Check vendors exist
    vendors = Vendor.objects.all()
    if not vendors.exists():
        return Response(
            {"error": "No vendors found in database"},
            status=status.HTTP_400_BAD_REQUEST
        )

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
