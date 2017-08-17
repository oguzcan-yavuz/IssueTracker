from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from issues.models import Issue


class AddIssueForm(forms.ModelForm):
    """
    We are creating new issues with this form
    """
    class Meta:
        model = Issue
        fields = ("name", "product", "tech_guy", "is_solved")


class UserForm(UserCreationForm):
    """
    Creates new technical support users
    """
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
