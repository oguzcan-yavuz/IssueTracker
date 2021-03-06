from django.conf.urls import url
from .views import *

# charts/
urlpatterns = [
    url(r'^$', ChartView.as_view(), name="chart_main"),
    # TODO: make rest endpoints global in website, not under charts app
    url(r'^rest/$', RestApiView.as_view(), name="rest"),
    url(r'^category_issue/$', CategoryIssueView.as_view(), name="category_issue_chart"),
    url(r'^customer_issue/$', CustomerIssueView.as_view(), name="customer_issue_chart"),
    url(r'^product_issue/$', ProductIssueView.as_view(), name="product_issue_chart"),
    url(r'^tech_guy_issue/$', TechGuyIssueView.as_view(), name="tech_guy_issue_chart"),
    # StatisticsView url
    url(r'^statistics/$', StatisticView.as_view(), name="profit_json"),
]
