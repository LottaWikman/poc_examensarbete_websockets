from django.shortcuts import render
from django.http import JsonResponse


def frontend_view(request):
    return render(request, "frontend_simulation.html")


def process_with_websocket(request):

    print("Hej")

    print("Ojdå")

    print("Hoppsan")

    return JsonResponse(
        {"status": "Success", "code": 200, "message": "A bunch of things happened"}
    )


def process_with_http(request):
    return JsonResponse(
        {"status": "Success", "code": 200, "message": "A bunch of things happened"}
    )
