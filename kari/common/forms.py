from kari.const import Const
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=Const.USERNAME_MAX_LENGTH)
    passwd = forms.CharField(widget=forms.PasswordInput, max_length=Const.PASSWD_MAX_LENGTH)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=Const.USERNAME_MAX_LENGTH)
    passwd1 = forms.CharField(widget=forms.PasswordInput, max_length=Const.PASSWD_MAX_LENGTH)
    passwd2 = forms.CharField(widget=forms.PasswordInput, max_length=Const.PASSWD_MAX_LENGTH)
