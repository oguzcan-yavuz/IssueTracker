from django.db import models
from django.conf import settings


class Issue(models.Model):
    STATUSES = (
        ('QU', 'IN QUEUE'),
        ('FI', 'FIXING'),
        ('DO', 'DONE'),
    )
    name = models.CharField(max_length=1000, unique=True, blank=True, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey('Product', related_name="broken_product", blank=True, null=True)
    tech_guy = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True)
    status = models.CharField(default='QU', max_length=2, choices=STATUSES)
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    customer_surname = models.CharField(max_length=100, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return "{0}: {1}".format(self.pk, self.name)

    class Meta:
        get_latest_by = "creation_time"


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey('Category', related_name="product")

    def __str__(self):
        return "{0}: {1} {2}".format(self.pk, self.name, self.category)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return "{0}: {1}".format(self.pk, self.name)

