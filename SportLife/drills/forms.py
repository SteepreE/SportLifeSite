import datetime

from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm

from .models import User
from django import forms


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True,
                                                           'class': 'form-control form-control-lg rounded-4'}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password",
                                          'class': 'form-control form-control-lg rounded-4'}),
    )


class UserRegistrationForm(UserCreationForm):

    birth_date = forms.DateField(
        label="Дата рождения",
        widget=forms.SelectDateWidget(attrs={'class': 'm-1'}, years=range(1900, datetime.date.today().year),)
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'birth_date', 'password1', 'password2']