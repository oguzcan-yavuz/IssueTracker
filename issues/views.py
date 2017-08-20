from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import *

from .forms import *
from .models import Issue


class CustomView(CreateView):
    title = "test"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["custom_title"] = self.title
        return context


class MainView(LoginRequiredMixin, ListView):
    context_object_name = 'issue_list'   # changes the variable name that passes to the template
    template_name = 'issues/index.html'
    queryset = Issue.objects.all().order_by("-creation_time")   # queryset = Issue.objects.all() | model = Issue


class IssueView(LoginRequiredMixin, UpdateView):
    """Shows details of the issue. Also works like an update view for updating the issue."""

    # it is not listing the issues but form is showing.
    model = Issue
    form_class = IssueForm
    template_name = "issues/issue_update.html"
    success_url = '/'


class AddIssueView(LoginRequiredMixin, CustomView):
    """
    Creates new issues.
    """
    form_class = AddIssueForm
    template_name = 'issues/basic_form.html'
    success_url = "/"
    title = "Yeni Sorun Ekle"     # test variable for template

    def form_valid(self, form):
        form.instance.tech_guy = self.request.user  # we are assigning tech_guy with request.user
        return super(AddIssueView, self).form_valid(form)


class AddCustomerView(LoginRequiredMixin, CustomView):
    """Creates new customers"""
    form_class = CustomerForm
    template_name = "issues/basic_form.html"
    success_url = "/"
    title = "Yeni Müşteri Ekle"

    def form_valid(self, form):
        form.instance.registered_by = self.request.user
        return super(AddCustomerView, self).form_valid(form)


class AddCategoryView(LoginRequiredMixin, CustomView):
    """Creates new categories"""
    form_class = CategoryForm
    template_name = "issues/basic_form.html"
    success_url = "/"
    title = "Yeni Kategori Ekle"


class AddProductView(LoginRequiredMixin, CustomView):
    """Creates new products"""
    form_class = ProductForm
    template_name = "issues/basic_form.html"
    success_url = "/"
    title = "Yeni Ürün Ekle"


class UserView(PermissionRequiredMixin, CustomView):
    """
    Creates new tech guys...
    """
    permission_required = 'user.is_superuser'
    form_class = UserForm
    template_name = "issues/register.html"
    success_url = "/"
