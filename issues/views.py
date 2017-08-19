from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *

from .forms import AddIssueForm, UserForm
from .models import Issue


class MainView(ListView):
    context_object_name = 'issue_list'   # changes the variable name that passes to the template
    template_name = 'issues/index.html'
    queryset = Issue.objects.all().order_by("-creation_time")   # queryset = Issue.objects.all() => model = Issue


class AddIssueView(LoginRequiredMixin, CreateView):
    """
    Creates new issues.
    """
    form_class = AddIssueForm
    template_name = 'issues/issue_add.html'
    success_url = "/"

    def form_valid(self, form):
        form.instance.tech_guy = self.request.user  # we are assigning tech_guy with request.user
        return super(AddIssueView, self).form_valid(form)


class UserView(CreateView):
    """
    Creates new tech guys...
    """
    form_class = UserForm
    template_name = "issues/register.html"
    success_url = "/"
