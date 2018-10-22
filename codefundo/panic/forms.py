from django import forms
import datetime

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget

from .models import Account


class SignUpForm(UserCreationForm):

    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'password1', 'password2')
