from django import forms

class SearchForm(forms.Form):
    topic = forms.CharField(label='Search', max_length=100)