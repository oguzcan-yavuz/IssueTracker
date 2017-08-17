from django import forms

from issues.models import Issue


class AddIssueForm(forms.ModelForm):
    """
    We are creating new issues with this form
    """
    class Meta:
        model = Issue
        fields = ("name", "product", "tech_guy", "is_solved")
