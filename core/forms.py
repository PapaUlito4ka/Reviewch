from django import forms
from core.models import User


class RegisterForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput
    )
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )
