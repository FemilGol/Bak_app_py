from django import forms
from django.contrib.auth.forms import UserCreationForm
import re

class SignUpForm(UserCreationForm):
    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise forms.ValidationError('Invalid email format')
        return email

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)