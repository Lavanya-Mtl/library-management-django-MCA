from django.forms import ModelForm
from .models import BookIssue


class BookIssueForm(ModelForm):
    class Meta:
        model = BookIssue
        fields = '__all__'