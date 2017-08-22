from django.conf.urls import url
from .views import *

# charts/
urlpatterns = [
    url(r'^$', ChartView.as_view(), name="chart_main"),
    url(r'^issue_chart/$', IssueChartView.as_view(), name="issue_chart"),
    url(r'^rest/$', RestApiView.as_view(), name="rest"),
    url(r'^rest/chart/$', ChartApiView.as_view(), name="chart_api"),
    url(r'^rest/issue_chart/$', IssueChartApiView.as_view(), name='issue_api'),
]
