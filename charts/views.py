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


class CustomerIssueView(LoginRequiredMixin, TemplateView):
    template_name = 'charts/customer_issue.html'


class ProductIssueView(LoginRequiredMixin, TemplateView):
    template_name = 'charts/product_issue.html'


class TechGuyIssueView(LoginRequiredMixin, TemplateView):
    template_name = 'charts/tech_guy_issue.html'


# returns all data for each model in issues.models

class RestApiView(LoginRequiredMixin, APIView):
    """This view uses django-rest-framework's api view to give certain statistics."""

    def get(self, request):
        if request.is_ajax():
            data = {}
            statistic = int(request.GET.get('statistic'))
            if statistic == 1:
                """This statistic gives all serialized data."""
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
                """This statistic gives count of each model."""
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

    def return_response(self, data):
        # We are doing serialization this way when our queryset is ValuesQuerySet.
        # Because regular django serializers can't serialize it.
        data = json.dumps(data, cls=DjangoJSONEncoder)
        return JsonResponse(data, safe=False)

    def statistic_1(self, first_date, last_date):
        """This statistic gives issues done in given date gaps."""
        data = Issue.objects.filter(delivery_time__gte=first_date,
                                    delivery_time__lte=last_date, status='DO')
        return JsonResponse(serializers.serialize('json', data), safe=False)

    def statistic_2(self, first_date, last_date):
        """This statistic gives the issues's count which grouped by categories
        in given date gap."""
        data = Issue.objects.filter(
            creation_time__gte=first_date, creation_time__lte=last_date).values(
            'product__category__name').annotate(count=Count('product__category'))
        # return JsonResponse(serializers.serialize('json', data), safe=False)
        return self.return_response(list(data))

    def statistic_3(self, first_date, last_date):
        """This statistic gives the customers's count which created issue in given
        date gap."""
        data = []
        current_date = first_date
        day = timedelta(days=1)

        while current_date <= last_date:
            current_date_range = current_date + day
            data.append([{'date': current_date}] + list(Issue.objects.filter(
                creation_time__range=(current_date, current_date_range)).values(
                'customer__name').annotate(
                customer_count=Count('customer'))))
            current_date += day
        return self.return_response(data)

    def statistic_4(self, first_date, last_date):
        """This statistic gives the products's count which have an issue in given
        date gap."""
        data = []
        current_date = first_date
        day = timedelta(days=1)

        while current_date <= last_date:
            current_date_range = current_date + day
            data.append([{'date': current_date}] + list(Issue.objects.filter(
                creation_time__range=(current_date, current_date_range)).values(
                'product__name').annotate(product_count=Count('product'))))
            current_date += day
        return self.return_response(data)

    def statistic_5(self):
        """This statistic gives the average time of problem solve of tech guys
        and count of problems they have solved."""
        data = Issue.objects.filter(status='DO').values('tech_guy__username').annotate(
            fix_time_avg=Avg(ExpressionWrapper(F('delivery_time') - F('creation_time'),
                                               output_field=DurationField())),
            solved_issue_count=Count('tech_guy')).order_by('fix_time_avg')
        return self.return_response(list(data))

    def get_static_functions_by_id(self, function_id, *args):
        functions = [self.statistic_1, self.statistic_2, self.statistic_3, self.statistic_4, self.statistic_5]
        if function_id > 5 or function_id < 1:
            return HttpResponseForbidden("<h1>403 FORBIDDEN</h1>")
        return functions[function_id - 1]() if function_id == 5 else functions[function_id - 1](args[0], args[1])

    def format_dates(self, date):
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
        date = timezone.make_aware(date, timezone.get_current_timezone())
        return date

    def get(self, request):
        if request.is_ajax():
            statistic = int(request.GET.get('statistic'))
            if statistic in [1, 2, 3, 4]:
                first_date = request.GET.get('first_date')
                last_date = request.GET.get('last_date')
                first_date, last_date = self.format_dates(first_date), self.format_dates(last_date)
                return self.get_static_functions_by_id(statistic, first_date, last_date)
            else:
                return self.get_static_functions_by_id(statistic)

        else:
            return HttpResponseForbidden("<h1>403 FORBIDDEN</h1>")
