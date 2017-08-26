from django.conf.urls import url
from .views import *

urlpatterns = [
    # ListView urls
    url(r'^$', IssueListView.as_view(), name="main"),
    url(r'^products/$', ProductListView.as_view(), name="product_list_url"),
    url(r'^customers/$', CustomerListView.as_view(), name="customer_list_url"),
    url(r'^categories/$', CategoryListView.as_view(), name="category_list_url"),
    # CustomerHistory url
    url(r'^customers/history/(?P<customer_id>\d+)/$', CustomerHistoryView.as_view(), name="customer_history"),
    # TechGuyHistory url
    url(r'^tech_guys/history/(?P<tech_guy_id>\d+)/$', TechGuysHistoryView.as_view(), name="tech_guy_history"),
    # StatisticsView url
    url(r'^statistics/$', StatisticView.as_view(), name="profit_json"),
    # ProfitView url
    url(r'^profits/$', ProfitTemplateView.as_view(), name="profits"),
    # CreateView urls
    url(r'^issues/add/issue/$', AddIssueView.as_view(), name="new_issue"),
    url(r'^issues/add/customer/$', AddCustomerView.as_view(), name="new_customer"),
    url(r'^issues/add/category/$', AddCategoryView.as_view(), name="new_category"),
    url(r'^issues/add/product/$', AddProductView.as_view(), name="new_product"),
    # UpdateView urls
    url(r"^issues/(?P<pk>\d+)/$", IssueUpdateView.as_view(), name="issue_update"),
    url(r"^products/(?P<pk>\d+)/$", ProductUpdateView.as_view(), name="product_update"),
    url(r"^customers/(?P<pk>\d+)/$", CustomerUpdateView.as_view(), name="customer_update"),
    url(r"^categories/(?P<pk>\d+)/$", CategoryUpdateView.as_view(), name="category_update"),
    # Registration url
    url(r'^register/$', UserView.as_view(), name="register"),
]
