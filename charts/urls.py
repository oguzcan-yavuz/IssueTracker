from django.conf.urls import url
from .views import *

# charts/
urlpatterns = [
    url(r'^$', HomeView.as_view(), name="chart_main"),
    url(r'^rest/$', ChartView.as_view()),
    url(r'^rest/(?P<pk>\d+)/$', ChartDetailView.as_view()),
]
