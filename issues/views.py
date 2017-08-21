from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import *
from django.shortcuts import reverse

from .forms import *
from .models import Issue


# ListViews

class IssueListView(LoginRequiredMixin, ListView):
    """Lists all issues"""
    context_object_name = 'issue_list'   # changes the variable name that passes to the template
    template_name = 'issues/index.html'
    queryset = Issue.objects.all().order_by("-creation_time")   # queryset = Issue.objects.all() | model = Issue
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
