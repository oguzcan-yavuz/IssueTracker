import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, F, ExpressionWrapper, Avg, DurationField
from django.http import HttpResponseForbidden, JsonResponse
from django.views.generic import TemplateView
from django.views import View
from django.utils import timezone

from datetime import datetime
from datetime import timedelta

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *


class ChartView(LoginRequiredMixin, TemplateView):
    template_name = 'charts/chart.html'


class CategoryIssueView(LoginRequiredMixin, TemplateView):
    template_name = 'charts/category_issue.html'


# returns all data for each model in issues.models

class RestApiView(LoginRequiredMixin, APIView):

    def get(self, request):
        if request.is_ajax():
            data = {}
            statistic = int(request.GET.get('statistic'))
            if statistic == 1:
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
            elif statistic == 2:
                labels = ["Sorun", "Müşteri", "Ürün", "Kategori"]
                values = [
                    Issue.objects.count(),
                    Customer.objects.count(),
                    Product.objects.count(),
                    Category.objects.count()
                ]
                data = {
                    'labels': labels,
                    'values': values,
                }
            return Response(data)
        else:
            return HttpResponseForbidden('<h1>403 FORBIDDEN</h1>')


# StatisticView

class StatisticView(LoginRequiredMixin, View):
    """Returns JSON data of asked statistic."""

    def get(self, request):
        if request.is_ajax():
            statistic = int(request.GET.get('statistic'))
            first_date = request.GET.get('first_date')
            last_date = request.GET.get('last_date')
            first_date = datetime.strptime(first_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            last_date = datetime.strptime(last_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            first_date = timezone.make_aware(first_date, timezone.get_current_timezone())
            last_date = timezone.make_aware(last_date, timezone.get_current_timezone())
            day = timedelta(days=1)

            if statistic == 1:
                """This statistic gives issues done in given date gaps."""
                data = Issue.objects.filter(delivery_time__gte=first_date,
                                            delivery_time__lte=last_date, status='DO')
                return JsonResponse(serializers.serialize('json', data), safe=False)
            elif statistic == 2:
                """This statistic gives the issues's count which grouped by categories
                in given date gap."""
                data = Issue.objects.filter(
                    creation_time__gte=first_date, creation_time__lte=last_date).values(
                    'product__category__name').annotate(count=Count('product__category'))

                # We are doing serialization this way when our queryset is ValuesQuerySet.
                # Because regular django serializers can't serialize it.
                data = json.dumps(list(data), cls=DjangoJSONEncoder)
                return JsonResponse(data, safe=False)
            elif statistic == 3:
                """This statistic gives the customers's count which created issue in given
                date gap."""
                data = []
                current_date = first_date

                while current_date <= last_date:
                    current_date_range = current_date + day
                    data.append(list(Issue.objects.filter(
                        creation_time__range=(current_date, current_date_range)).values(
                        'customer__name').annotate(count=Count('customer'))) + [{'date': current_date}])
                    current_date += day

                data = json.dumps(data, cls=DjangoJSONEncoder)
                return JsonResponse(data, safe=False)
            elif statistic == 4:
                """This statistic gives the products's count which have an issue in given
                date gap."""
                data = []
                current_date = first_date

                while current_date <= last_date:
                    current_date_range = current_date + day
                    data.append(Issue.objects.filter(
                        creation_time__range=(current_date, current_date_range)).values(
                        'product__name').annotate(count=Count('product')) + [{'date': current_date}])
                    current_date += day

                data = json.dumps(data, cls=DjangoJSONEncoder)
                return JsonResponse(data, safe=False)
            elif statistic == 5:
                """This statistic gives the average time of problem solve of tech guys
                and count of problems they have solved."""
                data = Issue.objects.filter(status='DO').values('tech_guy').annotate(
                    ort=Avg(ExpressionWrapper(F('delivery_time') - F('creation_time'),
                                              output_field=DurationField())),
                    count=Count('tech_guy')).order_by('ort')
                data = json.dumps(list(data), cls=DjangoJSONEncoder)
                return JsonResponse(data, safe=False)
        else:
            return HttpResponseForbidden("<h1>403 FORBIDDEN</h1>")


