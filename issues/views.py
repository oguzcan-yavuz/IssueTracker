from django.views.generic import *
from .models import Issue


class MainView(ListView):
    template_name = 'issues/index.html'

    def get_queryset(self):
        return list(Issue.objects.all().order_by("-creation_time")) if Issue.objects.all() else []
