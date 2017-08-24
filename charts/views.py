from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *


class ChartView(LoginRequiredMixin, TemplateView):
    template_name = 'charts/chart.html'


class IssueChartView(LoginRequiredMixin, TemplateView):
    template_name = 'charts/issue_chart.html'


# returns issue's delivery_time and creation_time difference to calculate it's fixing duration

class IssueChartApiView(LoginRequiredMixin, APIView):

    def get(self, request):
        if request.is_ajax():
            issue_fixing_durations = []
            for obj in Issue.objects.all():
                if obj.delivery_time is not None:
                    issue_fixing_durations.append((obj.delivery_time - obj.creation_time))
            issue_ids = [obj.id for obj in Issue.objects.all()]
            data = {
                "labels": issue_ids,
                "values": issue_fixing_durations,
            }
            return Response(data)
        else:
            return HttpResponseForbidden('<h1>403 FORBIDDEN</h1>')


# returns counts for each model in issues.models

class ChartApiView(LoginRequiredMixin, APIView):

    def get(self, request):
        if request.is_ajax():
            issues_count = Issue.objects.count()
            customers_count = Customer.objects.count()
            products_count = Customer.objects.count()
            categories_count = Category.objects.count()

            labels = ["Sorun", "Müşteri", "Ürün", "Kategori"]
            values = [issues_count, customers_count, products_count, categories_count]

            data = {
                "labels": labels,
                "values": values,
            }
            return Response(data)
        else:
            return HttpResponseForbidden('<h1>403 FORBIDDEN</h1>')


# returns all data for each model in issues.models

class RestApiView(LoginRequiredMixin, APIView):

    def get(self, request):
        if request.is_ajax():
            users = get_user_model().objects.all()
            issues = Issue.objects.all()
            customers = Customer.objects.all()
            products = Product.objects.all()
            categories = Category.objects.all()

            issue_serializer = IssueSerializer(issues, many=True)
            customer_serializer = CustomerSerializer(customers, many=True)
            product_serializer = ProductSerializer(products, many=True)
            category_serializer = CategorySerializer(categories, many=True)
            user_serializer = UserSerializer(users, many=True)

            data = {
                "issues": issue_serializer.data,
                "customers": customer_serializer.data,
                "products": product_serializer.data,
                "categories": category_serializer.data,
                "users": user_serializer.data
            }
            return Response(data)
        else:
            return HttpResponseForbidden('<h1>403 FORBIDDEN</h1>')
