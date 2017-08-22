from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer

from issues.models import *


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        User = get_user_model()
        model = User
        exclude = ('password',)
