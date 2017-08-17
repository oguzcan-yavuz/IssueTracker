from django.shortcuts import get_object_or_404
from django.views.generic import *
from django.urls import reverse

from forms import AddIssueForm
from .models import Issue


class MainView(ListView):
    template_name = 'issues/index.html'

    def get_queryset(self):
        return list(Issue.objects.all().order_by("-creation_time")) if Issue.objects.all() else []


class AddIssueView(CreateView):
    form_class = AddIssueForm
    template_name = 'issues/add_issue.html'
    success_url = "/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse("main")
    #
    # def get_form_kwargs(self):
    #     return super().get_form_kwargs()
    #
    # def get_context_data(self, **kwargs):
    #     return super().get_context_data()
    #
    # def post(self, request, *args, **kwargs):
    #     return super().post(request, *args, **kwargs)
