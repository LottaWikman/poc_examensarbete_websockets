from django.http import JsonResponse
from django.shortcuts import render


class Processor:

    def process_with_http(self):
        return JsonResponse({"status": "Klar"})
