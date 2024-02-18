"""
Module containing views for toll entry and exit endpoints.
"""

import datetime
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from toll_system.constants import BASE_TOLL_RATE, DISTANCE_RATE
from toll_system.utils import calculate_distance, calculate_toll, validate_datetime

from .models import TollData


@csrf_exempt
def entry(request):
    """
    View for handling entry requests.

    Accepts POST requests with JSON data containing the following fields:
    - interchange:
    - number_plate:
    - entry_time: (Optional)
    """

    if request.method == "POST":
        # Get the raw JSON data from the request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        # Extract parameters from the JSON data
        entry_interchange = data.get("interchange")
        number_plate = data.get("number_plate")
        entry_time = data.get("entry_time")

        # Check for missing required fields
        if not entry_interchange or not number_plate:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        # Validate and parse entry_time if provided
        if entry_time:
            try:
                entry_time = validate_datetime(entry_time)
            except ValueError as e:
                return JsonResponse({"error": str(e)}, status=400)
        else:
            # If entry_time is not provided, use current time
            entry_time = datetime.datetime.now()

        # Retrieve entry data
        entry_data = (
            TollData.objects.filter(
                exit_interchange__isnull=True, number_plate=number_plate
            )
            .order_by("-entry_time")
            .first()
        )
        if entry_data:
            entry_data.entry_interchange = entry_interchange
            entry_data.entry_time = entry_time
            entry_data.save()
        else:
            # Save entry data to PostgreSQL database
            TollData.objects.create(
                entry_interchange=entry_interchange,
                number_plate=number_plate,
                entry_time=entry_time,
            )
        return JsonResponse({"message": "Entry recorded successfully"}, status=201)


@csrf_exempt
def exit(request):
    """
    View for handling exit requests.

    Accepts POST requests with JSON data containing the following fields:
    - interchange:
    - number_plate:
    - exit_time:
    """

    if request.method == "POST":
        # Get the raw JSON data from the request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        # Extract parameters from the JSON data
        exit_interchange = data.get("interchange")
        number_plate = data.get("number_plate")
        exit_time = data.get("exit_time")
        if exit_time:
            try:
                exit_time = validate_datetime(exit_time)
            except ValueError as e:
                return JsonResponse({"error": str(e)}, status=400)
        else:
            exit_time = datetime.datetime.now()

        # Retrieve entry data
        entry_data = (
            TollData.objects.filter(
                exit_interchange__isnull=True, number_plate=number_plate
            )
            .order_by("-entry_time")
            .first()
        )

        if entry_data:
            entry_data.exit_interchange = exit_interchange
            entry_data.exit_time = exit_time
            entry_data.save()

            # Calculate toll
            total_toll = calculate_toll(
                entry_data.entry_interchange,
                exit_interchange,
                entry_data.entry_time,
                exit_time,
                number_plate,
            )
            distance = calculate_distance(
                entry_data.entry_interchange, exit_interchange
            )
            base_rate = BASE_TOLL_RATE
            distance_cost = distance * DISTANCE_RATE
            sub_total = base_rate + distance_cost
            discount = sub_total - total_toll

            response = {
                "Base Rate": base_rate,
                "Distance Cost Breakdown": distance_cost,
                "Sub-Total": sub_total,
                "Discount/Other": discount,
                "Total": total_toll,
            }

            return JsonResponse(response, status=200)
        else:
            return JsonResponse(
                {
                    "error": "No entry found for the given number plate or exit already recorded"
                },
                status=404,
            )
