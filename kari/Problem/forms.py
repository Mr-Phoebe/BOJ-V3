# -*- coding: utf-8 -*-

from django import forms
from ckeditor.widgets import CKEditorWidget

class addProblemForm(forms.Form):
    PROB_PRIV_CH = (
            ('private','只有自己可见'),  #only the author may view and modify it outside the contest
            ('protected','所有教师可见'),  #the admin with the same root as the author may view and modify it
            ('public','公开'),  #the admin with the same root as the author may view and modify it, with all user may view it outside
            #('ext','ext'),  #more complex privilege
            #if more complex privilege needed, you may add it here
            )
    SPJ_CH = (
            ('0', u'否'),
            ('1', u'是'),
            )

    prob_title = forms.CharField(max_length=128, initial='Untitled', label=u'题目标题')
    prob_priv = forms.ChoiceField(choices=PROB_PRIV_CH, label=u'题目权限')
    prob_time = forms.IntegerField(initial=1000, label=u'时间限制 (ms)')
    prob_memory = forms.IntegerField(initial=65536, label=u'内存限制 (kb)', max_value=1073741824)
    prob_codelength = forms.IntegerField(initial=65536, label=u'代码长度限制 (b)')
    prob_desc = forms.CharField(widget=CKEditorWidget(), label=u'题目描述' )
    prob_input_desc = forms.CharField(widget=CKEditorWidget(), label=u'输入描述')
    prob_output_desc = forms.CharField(widget=CKEditorWidget(), label=u'输出描述')
##    prob_desc = forms.CharField(widget=forms.Textarea(attrs={'class':'ckeditor'}), label=u'题目描述' )
##    prob_input_desc = forms.CharField(widget=forms.Textarea(attrs={'class':'ckeditor'}), label=u'输入描述')
##    prob_output_desc = forms.CharField(widget=forms.Textarea(attrs={'class':'ckeditor'}), label=u'输出描述')
    prob_input_sample = forms.CharField(widget=forms.Textarea, label=u'输入样例')
    prob_output_sample = forms.CharField(widget=forms.Textarea, label=u'输出样例')
    is_spj = forms.ChoiceField(choices=SPJ_CH, label=u'是否需要Special Judge')
    change_data = forms.ChoiceField(initial='1', choices=SPJ_CH, label=u'是否需要修改数据')
    #course_id = forms.IntegerField( label=u'课程')
#    file_in = forms.FileField(label=u'上传输入数据')
#    file_out = forms.FileField(label=u'上传输出数据')

#class uploadDataForm(form.Form):

