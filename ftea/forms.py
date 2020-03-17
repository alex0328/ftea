from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from ftea import models


class TranslateForm(forms.Form):
    Word_pol = forms.CharField(max_length=500, required=False)
    Word_eng = forms.CharField(max_length=500, required=False)


