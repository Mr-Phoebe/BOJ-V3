# coding: utf-8
from django import forms
from Register.const import Const

class ContestantForm(forms.Form):
    name        = forms.CharField(max_length = 35)
    gender      = forms.CharField(max_length = 10)
    grade       = forms.CharField(max_length = 20)
    school      = forms.CharField(max_length = 50)
    student_id  = forms.CharField(max_length = 15)
    class_id    = forms.CharField(max_length = 15)
    email       = forms.CharField(max_length = 50)
    mobile      = forms.CharField(max_length = 15)
    info        = forms.CharField(max_length = 500)

class TeamRegisterForm(forms.Form):
    name    = forms.CharField(max_length = Const.TEAM_NAME_MAX_LENGTH)
    passwd1 = forms.CharField(max_length = Const.PASSWD_MAX_LENGTH)
    passwd2 = forms.CharField(max_length = Const.PASSWD_MAX_LENGTH)

class TeamLoginForm(forms.Form):
    name    = forms.CharField(max_length = Const.TEAM_NAME_MAX_LENGTH)
    passwd  = forms.CharField(max_length = Const.PASSWD_MAX_LENGTH)
