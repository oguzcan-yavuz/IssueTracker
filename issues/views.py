import json

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse, HttpResponseForbidden
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.shortcuts import reverse
from django.db.models import Count, Max, F, ExpressionWrapper, Avg, DurationField

from .forms import *
from .models import Issue

from datetime import datetime


# ListViews

class IssueListView(LoginRequiredMixin, ListView):
    """Lists all issues"""
    context_object_name = 'issue_list'   # changes the variable name that passes to the template
    template_name = 'issues/index.html'
    queryset = Issue.objects.all().order_by("-creation_time")
    paginate_by = 10


class ProductListView(LoginRequiredMixin, ListView):
    """Lists all products"""
    context_object_name = 'product_list'
    template_name = 'issues/products.html'
    model = Product
    paginate_by = 10


class CustomerListView(LoginRequiredMixin, ListView):
    """Lists all customers"""
    context_object_name = 'customer_list'
    template_name = 'issues/customers.html'
    queryset = Customer.objects.all().order_by("-creation_time")
    paginate_by = 10


class CategoryListView(LoginRequiredMixin, ListView):
    """Lists all categories"""
    context_object_name = 'category_list'
    template_name = 'issues/categories.html'
    model = Category
    paginate_by = 10


# CustomerHistoryView

class CustomerHistoryView(LoginRequiredMixin, ListView):
    """lists specific customer's issues"""
    template_name = 'issues/customer_histories.html'
    context_object_name = 'customer_history'
    paginate_by = 10

    def get_queryset(self):
        customer_id = self.kwargs['customer_id']
        return Issue.objects.filter(customer_id=customer_id)


# StatisticView

class StatisticView(LoginRequiredMixin, View):
    """Returns JSON data of asked statistic."""

    def get(self, request):
        if request.is_ajax():

            def values_queryset_to_json(value):
                # We are doing serialization this way when our queryset is ValuesQuerySet.
                # Because regular django serializers can't serialize it.
                value = json.dumps(list(value), cls=DjangoJSONEncoder)
                return JsonResponse(value, safe=False)

            statistic = int(request.GET.get('statistic'))
            first_date = request.GET.get('first_date')
            last_date = request.GET.get('last_date')
            first_date = datetime.strptime(first_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            last_date = datetime.strptime(last_date, "%Y-%m-%dT%H:%M:%S.%fZ")
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
                return values_queryset_to_json(data)
            elif statistic == 3:
                """This statistic gives the customers's count which created issue in given
                date gap."""
                data = Issue.objects.filter(
                    creation_time__gte=first_date, creation_time__lte=last_date).values(
                    'customer').distinct().count()
                return values_queryset_to_json(data)
            elif statistic == 4:
                """This statistic gives the customers which ordered by their issue count."""
                data = Issue.objects.values('customer').annotate(count=Count('customer'))
                return values_queryset_to_json(data)
            elif statistic == 5:
                """This statistic gives the most trouble products."""
                data = Issue.objects.values('product').annotate(count=Count('product'))
                return values_queryset_to_json(data)
            elif statistic == 6:
                """This statistic gives the average time of problem solve of tech guys
                and count of problems they have solved."""
                data = Issue.objects.filter(status='DO').values('tech_guy').annotate(
                    ort=Avg(ExpressionWrapper(F('delivery_time') - F('creation_time'),
                                              output_field=DurationField()))).order_by('ort').annotate(
                    count=Count('tech_guy'))
                return values_queryset_to_json(data)
        else:
            return HttpResponseForbidden("<h1>403 FORBIDDEN</h1>")


# ProfitTemplateView

class ProfitTemplateView(LoginRequiredMixin, TemplateView):
    """Lists profit value between given dates."""
    template_name = 'issues/profits.html'


# Base UpdateView

class CustomUpdateView(LoginRequiredMixin, UpdateView):
    """Base update view"""
    template_name = 'issues/basic_update.html'
    title = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["custom_title"] = self.title
        return context


# UpdateViews

class IssueUpdateView(CustomUpdateView):
    """Updates the issue"""
    model = Issue
    form_class = IssueUpdateForm
    success_url = '/'
    title = "Sorun"
    context_object_name = "current_issues"


class ProductUpdateView(CustomUpdateView):
    """Updates the product"""
    model = Product
    form_class = ProductUpdateForm
    success_url = "/"
    title = "Ürün"


class CustomerUpdateView(CustomUpdateView):
    """Updates the customer"""
    model = Customer
    form_class = CustomerUpdateForm
    success_url = "/"
    title = "Müşteri"


class CategoryUpdateView(CustomUpdateView):
    """Updates the category"""
    model = Category
    form_class = CategoryUpdateForm
    success_url = "/"
    title = "Kategori"


# Base CreateView

class CustomView(LoginRequiredMixin, CreateView):
    """Base view for Issue, Product, Customer and Category CreateViews."""
    template_name = "issues/basic_form.html"
    title = ""
    redirect_url = "main"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["custom_title"] = self.title
        context["redirect_url"] = self.redirect_url
        return context


# CreateViews

class AddIssueView(CustomView):
    """Creates new issues."""
    form_class = AddIssueForm
    success_url = "/"
    title = "Yeni Sorun Ekle"
    redirect_url = "main"

    def form_valid(self, form):
        form.instance.tech_guy = self.request.user  # we are assigning tech_guy with request.user
        return super(AddIssueView, self).form_valid(form)


class AddCustomerView(CustomView):
    """Creates new customers"""
    form_class = CustomerForm
    title = "Yeni Müşteri Ekle"
    redirect_url = "new_product"

    def get_success_url(self):
        return reverse('new_product')

    def form_valid(self, form):
        form.instance.registered_by = self.request.user
        return super(AddCustomerView, self).form_valid(form)


class AddCategoryView(CustomView):
    """Creates new categories"""
    form_class = CategoryForm
    title = "Yeni Kategori Ekle"
    success_url = '/'


class AddProductView(CustomView):
    """Creates new products"""
    form_class = ProductForm
    title = "Yeni Ürün Ekle"
    redirect_url = "new_issue"

    def get_success_url(self):
        return reverse('new_issue')


# Registration (superuser only)

class UserView(PermissionRequiredMixin, CustomView):
    """Creates new tech guys..."""
    permission_required = 'user.is_superuser'
    form_class = UserForm
    template_name = "issues/register.html"
    success_url = "/"
