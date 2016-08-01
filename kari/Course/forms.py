# -*- coding: utf-8 -*-
from django import forms
from kari.const import Const
from Course.models import Course
from User.models import User

class modifyCourseForm( forms.Form):
    """
    form used to create and update courses
    """
    SCHOOL_ID_NOT_EXIST = u'编号为{0}的学院不存在'
    ADMIN_NOT_EXIST = u'用户名为{0}的管理员不存在'

    # school_id = forms.IntegerField( label=u'学院编号')
    # admin_name = forms.CharField( max_length=100, required=False, label=u'管理员')
    no = forms.CharField( max_length=100, label=u'课程标识符')
    name = forms.CharField( max_length=100, label=u'课程名称')
    
    def __init__( self, user_list=None, *args, **kwargs):
        super( modifyCourseForm, self).__init__( *args, **kwargs)
        self.fields['admin'] = forms.ModelChoiceField(
                queryset = user_list,
                required = False,
                # initial = False,
                # empty_label = None,
                label= u'管理员',
                widget=forms.Select(attrs={'class':'input-small'})
                )

    #def clean( self):
    #    """
    #    override clean method of CourseForm
    #    """

    #    cleaned_data = super( modifyCourseForm, self).clean()
    #    unhandled_admin_name = cleaned_data.get('admin_name')
    #    if unhandled_admin_name:
    #        try:
    #            unhandled_admin = User.getUserByRawUsername( unhandled_admin_name)
    #        except:
    #            raise forms.ValidationError( self.ADMIN_NOT_EXIST.format( unhandled_admin_name))
    #        if not unhandled_admin:
    #            raise forms.ValidationError( self.ADMIN_NOT_EXIST.format( unhandled_admin_name))

    #    return cleaned_data

class courseListForm( forms.Form):
    """
    form used to filter Course List 
    """

    # school_id = forms.IntegerField( required=False, label=u'学院编号')
    # admin_id = forms.IntegerField( required=False, label=u'管理员编号')
    admin_name = forms.CharField( required=False, label=u'管理员名称')
    name = forms.CharField( required=False, max_length=100, label=u'课程名称')
    no = forms.CharField( required=False, max_length=100, label=u'课程标识符')

class modifyCourseClassForm( forms.Form):
    """
    form used to create and update course_classes
    """
    COURSE_ID_NOT_EXIST = u'编号为{0}的课程不存在'
    ADMIN_NOT_EXIST = u'用户名为{0}的管理员不存在'

    # course_id = forms.IntegerField( label=u'课程编号')
    # groups_id = forms.IntegerField( label=u'学院编号')
    # how to use many_to_many field in form
    # admin_name = forms.CharField( max_length=100, label=u'管理员')
    name = forms.CharField( max_length=100, label=u'课程开班名称')
    year = forms.IntegerField( label=u'课程开设年份')

    def __init__( self, user_list=None, *args, **kwargs):
        super( modifyCourseClassForm, self).__init__( *args, **kwargs)
        self.fields['admin'] = forms.ModelChoiceField(
                queryset = user_list,
                required = True,
                # initial = user_list[0],
                empty_label = None,
                label= u'管理员',
                widget=forms.Select(attrs={'class':'input-small'})
                )
    
    #def clean( self):
    #    """
    #    override clean method of CourseClassForm
    #    """

    #    cleaned_data = super( modifyCourseClassForm, self).clean()
    #    unhandled_admin_name = cleaned_data.get('admin_name')
    #    try:
    #        unhandled_admin = User.getUserByRawUsername( unhandled_admin_name)
    #    except:
    #        raise forms.ValidationError( self.ADMIN_NOT_EXIST.format( unhandled_admin_name))
    #    if not unhandled_admin:
    #        raise forms.ValidationError( self.ADMIN_NOT_EXIST.format( unhandled_admin_name))

    #    return cleaned_data

class courseClassListForm( forms.Form):
    """
    form used to filter CourseClass List 
    """

    # course_id = forms.IntegerField( required=False, label=u'课程编号')
    # groups_id = forms.IntegerField( label=u'学院编号')
    # admin_id = forms.IntegerField( required=False, label=u'管理员编号')
    admin_name = forms.CharField( required=False, label=u'管理员名称')
    name = forms.CharField( required=False, max_length=100, label=u'课程开班名称')
    year = forms.IntegerField( required=False, label=u'课程开设年份')
