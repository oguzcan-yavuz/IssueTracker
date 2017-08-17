from django.db import models
from django.conf import settings


class Issue(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey('Product', related_name="broken_product")
    tech_guy = models.ForeignKey(settings.AUTH_USER_MODEL)
    is_solved = models.BooleanField(default=False)

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
