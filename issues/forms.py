from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import HiddenInput

from issues.models import *


# New model creation forms

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


# Update Forms

class IssueUpdateForm(forms.ModelForm):
    """Updates the issue"""
    class Meta:
        model = Issue
        fields = ('name', 'delivery_time', 'status', 'price', 'todo_list', 'done_list')


class ProductUpdateForm(forms.ModelForm):
    """Updates the product"""
    class Meta:
        model = Product
        exclude = tuple()


class CustomerUpdateForm(forms.ModelForm):
    """Updates the customer"""
    class Meta:
        model = Customer
        exclude = ('creation_time', 'registered_by')


class CategoryUpdateForm(forms.ModelForm):
    """Updates the category"""
    class Meta:
        model = Category
        exclude = tuple()


# Registration Form

class UserForm(UserCreationForm):
    """Creates new technical support users"""
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

