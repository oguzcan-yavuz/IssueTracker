from django.db import models
from django.conf import settings


# Issue

class Issue(models.Model):
    """Issue model has relation with Product and Customer models with ForeignKey."""
    STATUSES = (
        ('QU', 'IN QUEUE'),
        ('FI', 'FIXING'),
        ('RE', 'RETURN'),
        ('CE', 'COMPONENTS EXPECTED'),
        ('DO', 'DONE'),
    )
    name = models.CharField(max_length=1000)
    creation_time = models.DateTimeField(auto_now_add=True)
    delivery_time = models.DateTimeField(blank=True, null=True)
    product = models.ForeignKey('Product', related_name="broken_product")
    tech_guy = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True)
    status = models.CharField(default='QU', max_length=2, choices=STATUSES)
    price = models.CharField(default="0", max_length=20)
    customer = models.ForeignKey("Customer")
    todo_list = models.TextField(blank=True, null=True)
    done_list = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{0}: {1}".format(self.pk, self.name)


# Customer

class Customer(models.Model):
    """Customer model has relation with User model(ForeignKey) to keep who registered them."""
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


# Product

class Product(models.Model):
    """Product model has relation with Category model with ForeignKey."""
    COLORS = (
        ("red", "KIRMIZI"),
        ("green", "YEŞİL"),
        ("blue", "MAVİ"),
        ("white", "BEYAZ"),
        ("black", "SİYAH"),
        ("brown", "KAHVERENGİ"),
        ("purple", "MOR"),
        ("orange", "TURUNCU"),
    )

    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey('Category', related_name="product")
    serial_number = models.CharField(max_length=25, blank=True, null=True)
    case_status = models.TextField(blank=True, null=True)
    warranty = models.BooleanField(default=False)
    color = models.CharField(max_length=20, choices=COLORS, blank=True, null=True)

    def __str__(self):
        return "{0}".format(self.name)


# Category

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return "{0}".format(self.name)
