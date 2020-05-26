from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Creating a new form that extends the django form
class UserRegisterForm(UserCreationForm):
    # Field to add
    email = forms.EmailField()

    # The meta class says what model will be affected and what field to display and in what order
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
