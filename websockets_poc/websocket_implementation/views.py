from django.shortcuts import render
from django.http import JsonResponse
import time
from .consumers import broadcast_progress, active_connections


def frontend_view(request):
    return render(request, "frontend_simulation.html")


def process_with_websocket(request):

    # Get connection_id from frontend
    connection_id = request.GET.get("connection_id")

    if not connection_id or connection_id not in active_connections:
        return JsonResponse(
            {"status": "Error", "message": "Invalid WebSocket connection"}, status=400
        )

    # Add connection_id to each broadcast_progress-call because we only
    # want to broadcast to this specific connection_id!
    broadcast_progress("0 % Initiating process", connection_id)

    # Simulate response time from microservice
    time.sleep(1)

    broadcast_progress("25 % Working through the process.", connection_id)

    time.sleep(1)

    broadcast_progress("50 % Halfway done.", connection_id)

    time.sleep(1)

    broadcast_progress("75 % Going through the last steps...", connection_id)

    time.sleep(1)

    return JsonResponse(
        {
            "status": "Success",
            "code": 200,
            "message": "100 % Process completed.",
        }
    )


def process_with_http(request):

    messages_to_frontend = []

    messages_to_frontend.append("0 % Initiating process")

    # Simulate response time from microservice
    time.sleep(1)

    messages_to_frontend.append("25 % Working through the process.")

    time.sleep(1)

    messages_to_frontend.append("50 % Halfway done.")

    time.sleep(1)

    messages_to_frontend.append("75 % Going through the last steps...")

    time.sleep(1)

    messages_to_frontend.append("100 % Process completed.")

    return JsonResponse(
        {
            "status": "Success",
            "code": 200,
            "message": messages_to_frontend,
        }
    )
