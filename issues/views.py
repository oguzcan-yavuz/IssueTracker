from django.views.generic import *

from .forms import AddIssueForm, UserForm
from .models import Issue


class MainView(ListView):
    template_name = 'issues/index.html'

    def get_queryset(self):
        return list(Issue.objects.all().order_by("-creation_time")) if Issue.objects.all() else []


class AddIssueView(CreateView):
    """
    Creates new issues.
    """
    form_class = AddIssueForm
    template_name = 'issues/add_issue.html'
    success_url = "/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UserView(CreateView):
    """
    Creates new tech guys...
    """
    form_class = UserForm
    template_name = "issues/register.html"
    success_url = "/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
