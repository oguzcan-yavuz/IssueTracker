from django.views.generic import ListView
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response

from issues.models import *


class HomeView(ListView):
    template_name = 'charts/chart.html'


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        User = get_user_model()
        labels = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]
        values = [12, 21, 31, 43, 57, 3]
        data = {
            "labels": labels,
            "values": values,
            "issue_names": [issue.name for issue in Issue.objects.all()],
            "product_names": [product.name for product in Product.objects.all()],
            "customer_names": [customer.name for customer in Customer.objects.all()],
            "category_names": [category.name for category in Category.objects.all()],
            "users": [user.username for user in User.objects.all()]
        }
        return Response(data)

