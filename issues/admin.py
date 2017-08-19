from django.contrib import admin
from issues.models import *

admin.site.register(Issue)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer)
