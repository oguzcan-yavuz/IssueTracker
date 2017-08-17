from django.contrib import admin
from issues.models import Issue, Product, Category

admin.site.register(Issue)
admin.site.register(Product)
admin.site.register(Category)
