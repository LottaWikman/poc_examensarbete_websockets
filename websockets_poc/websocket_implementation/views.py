from django.shortcuts import render
from django.http import JsonResponse
import time
from .consumers import broadcast_progress


def frontend_view(request):
    return render(request, "frontend_simulation.html")


def process_with_websocket(request):

    # Simulate response time from microservice
    time.sleep(1)

    broadcast_progress("1. Initiating process")

    time.sleep(1)

    broadcast_progress("2. In the beginning of the process")

    time.sleep(1)

    broadcast_progress("3. Now we're getting somewhere")

    time.sleep(1)

    broadcast_progress("4. Almost done...")

    time.sleep(1)

    return JsonResponse(
        {
            "status": "Success",
            "code": 200,
            "message": "Done!",
        }
    )


def process_with_http(request):

    messages_to_frontend = []

    messages_to_frontend.append("1. Initiating process")

    # Simulate response time from microservice
    time.sleep(1)

    messages_to_frontend.append("2. In the beginning of the process")

    time.sleep(1)

    messages_to_frontend.append("3. Now we're getting somewhere")

    time.sleep(1)

    messages_to_frontend.append("4. Almost done...")

    time.sleep(1)

    print(f"message_to_frontend : {messages_to_frontend}")

    return JsonResponse(
        {
            "status": "Success",
            "code": 200,
            "message": messages_to_frontend,
        }
    )
