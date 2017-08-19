from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', MainView.as_view(), name="main"),
    url(r'^issues/$', AddIssueView.as_view(), name="new_issue"),
    url(r'^register/$', UserView.as_view(), name="register"),
    url(r'^customers/$', AddCustomerView.as_view(), name="new_customer"),
    url(r'^categories/$', AddCategoryView.as_view(), name="new_category"),
    url(r'^products/$', AddProductView.as_view(), name="new_product"),
]
