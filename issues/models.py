from django.db import models
from django.conf import settings


class Issue(models.Model):
    STATUSES = (
        ('QU', 'IN QUEUE'),
        ('FI', 'FIXING'),
        ('DO', 'DONE'),
    )
    name = models.CharField(max_length=1000)
    creation_time = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey('Product', related_name="broken_product")
    tech_guy = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True)
    status = models.CharField(default='QU', max_length=2, choices=STATUSES)
    price = models.CharField(default="0", max_length=20)
    customer = models.ForeignKey("Customer")
    todo_list = models.TextField(blank=True, null=True)
    done_list = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{0}: {1}".format(self.pk, self.name)


class Customer(models.Model):
    GENDERS = (
        ("M", "MALE"),
        ("F", "FEMALE")
    )
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    creation_time = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    tax_number = models.CharField(max_length=20, blank=True, null=True)
    id_number = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDERS, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    registered_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return "{0}".format(self.name)


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey('Category', related_name="product")

    def __str__(self):
        return "{0}: {1} {2}".format(self.pk, self.name, self.category)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return "{0}: {1}".format(self.pk, self.name)

