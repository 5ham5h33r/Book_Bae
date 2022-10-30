from django import forms

# Create your models here.


class SearchQuery(forms.Form):
    name = forms.CharField(max_length=100)
