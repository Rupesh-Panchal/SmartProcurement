from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor
import math

@api_view(['POST'])
def optimize_order(request):
    required_length = request.data.get("required_length")
    quantity = request.data.get("quantity")

    # ✅ Input validation
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
            {"error": "Inputs must be integers"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if required_length <= 0 or quantity <= 0:
        return Response(
            {"error": "Values must be greater than zero"},
            status=status.HTTP_400_BAD_REQUEST
        )

    RAW_TUBE_LENGTH = 6000

    pieces_per_tube = RAW_TUBE_LENGTH // required_length
    if pieces_per_tube == 0:
        return Response(
            {"error": "Required length too large"},
            status=status.HTTP_400_BAD_REQUEST
        )

    raw_tubes_required = math.ceil(quantity / pieces_per_tube)

    vendors = Vendor.objects.all()
    if not vendors.exists():
        return Response(
            {"error": "No vendors found"},
            status=status.HTTP_400_BAD_REQUEST
        )

    vendor_results = []
    best_vendor = None
    lowest_cost = None

    for vendor in vendors:
        total_cost = vendor.price_per_tube * raw_tubes_required

        vendor_results.append({
            "name": vendor.name,
            "total_cost": total_cost,
            "delivery_days": vendor.delivery_days,
        })

        if lowest_cost is None or total_cost < lowest_cost:
            lowest_cost = total_cost
            best_vendor = vendor
        elif total_cost == lowest_cost and vendor.delivery_days < best_vendor.delivery_days:
            best_vendor = vendor

    # ✅ Mark best vendor
    for v in vendor_results:
        v["is_best"] = (v["name"] == best_vendor.name)

    return Response({
        "raw_tubes_required": raw_tubes_required,
        "vendors": vendor_results
    }, status=status.HTTP_200_OK)
