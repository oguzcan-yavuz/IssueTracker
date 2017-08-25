from django.conf.urls import url
from .views import *

# charts/
urlpatterns = [
    url(r'^$', ChartView.as_view(), name="chart_main"),
    url(r'^issue_charts/$', IssueChartView.as_view(), name="issue_chart"),
    # make rest endpoints global in website, not under charts app
    url(r'^rest/$', RestApiView.as_view(), name="rest"),
    url(r'^rest/chart/$', ChartApiView.as_view(), name="chart_api"),
    url(r'^rest/issue_chart/$', IssueChartApiView.as_view(), name='issue_api'),
    url(r'^category_issue/$', CategoryIssueView.as_view(), name="category_issue_chart"),
]
