# coding: utf-8
from django import forms
from User.models import *
from kari.const import Const
from django.core.exceptions import ValidationError

errmsg = {'required':u'必填项目！'}
class LoginForm(forms.Form):
    username = forms.CharField(max_length=Const.USERNAME_MAX_LENGTH, required=True, label=u'用户名', error_messages=errmsg)
    passwd = forms.CharField(widget=forms.PasswordInput, max_length=Const.PASSWD_MAX_LENGTH, required=True, label=u'密码', error_messages=errmsg)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()

        usname = cleaned_data.get('username')
        pswd = cleaned_data.get('passwd')
        u = User.getUserByRawUsername(usname)
        if u == False:
            raise ValidationError(Const.LOGIN_FAIL)
            # self._errors['username'] = Const.USERNAME_NOT_EXIST
        elif not u._chkPasswd(pswd):
            raise ValidationError(Const.LOGIN_FAIL)
        return cleaned_data

class AddSchoolForm(forms.Form):
    schoolabbr = forms.CharField(max_length=30, required=True, label=u'学院简称', error_messages=errmsg)
    schoolname = forms.CharField(max_length=30, required=True, label=u'学院名称', error_messages=errmsg)

class ModifyGroupForm(forms.Form):
    name = forms.CharField(max_length=30, required=True,
            label=u'班级号', widget=forms.TextInput(attrs={
                #'class':'input-block-level',
                'placeholder':u'班级号',
                }))

    def __init__(self, schools, *args, **kwargs):
        super(ModifyGroupForm, self).__init__(*args, **kwargs)
        self.fields['school'] = forms.ModelChoiceField(empty_label=None,
                label=u'所属学院', required=True,
                queryset=schools, widget=forms.Select(attrs={
                    #'class':'input-block-level',
                    }))

class AddMultiUserForm(forms.Form):
    pass

class SearchUserForm(forms.Form):
    username = forms.CharField(max_length=Const.USERNAME_MAX_LENGTH, required=False, label=u'学号', error_messages=errmsg)

