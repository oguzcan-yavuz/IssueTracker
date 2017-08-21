from django.shortcuts import render
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charts/chart.html', {})


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]
        values = [12, 21, 31, 43, 57, 3]
        data = {
            "labels": labels,
            "values": values,
        }
        return Response(data)

