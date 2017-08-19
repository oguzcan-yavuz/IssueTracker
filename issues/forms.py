from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import HiddenInput

from issues.models import *


class AddIssueForm(forms.ModelForm):
    """Creates new issues."""
    class Meta:
        model = Issue
        exclude = tuple('creation_time')
        widgets = {
            "tech_guy": HiddenInput(),
        }


class CustomerForm(forms.ModelForm):
    """Creates new customers."""
    class Meta:
        model = Customer
        exclude = tuple('creation_time')
        widgets = {
            "registered_by": HiddenInput()
        }


class ProductForm(forms.ModelForm):
    """Creates new products."""
    class Meta:
        model = Product
        fields = ('name', 'category')


class CategoryForm(forms.ModelForm):
    """Creates new categories."""
    class Meta:
        model = Category
        fields = ('name',)


class UserForm(UserCreationForm):
    """Creates new technical support users"""
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

