# -*- coding: utf-8 -*-
from django import forms
from datetime import datetime
from kari.const import Const
from Submission.models import Submission

class addSubmissionForm( forms.Form):
    """
    form used to submit codes
    """

    # cid = forms.IntegerField( required=False,label=u'考试编号')
    # pid = forms.IntegerField( required=False,label=u'题目编号')
    #input_or_upload = forms.ChoiceField( choices=SUBMIT_METHOD, initial='0', label=u'选择提交方式')
    code = forms.CharField( required=False, widget=forms.Textarea(attrs={'class':'input-block-level kari-code'}), label=u'或者直接粘贴代码')
    code_file = forms.FileField( required=False, label=u'上传代码')
    def __init__(self, langList, *args, **kwargs):
        super(addSubmissionForm, self).__init__(*args, **kwargs)
        self.fields['language'] = forms.ChoiceField(
                choices=langList, initial=(langList[0][0] if len(langList)>0 else None),
                label=u'选择语言',widget=forms.Select(attrs={'class':'input-medium'}))

class submissionListForm( forms.Form):
    """
    form used to filter Submission List 
    """

    STATUS = [
            ('', u'结果'), # value first, label second
            ('Accepted', u'通过'),
            ('Presentation Error', u'格式错误'),
            ('Wrong Answer', u'答案错误'),
            ('Time Limit Exceed', u'超过时间限制'),
            ('Memory Limit Exceed', u'超过内存限制'),
            ('Runtime Error', u'运行时错误'),
            ('Compile Error', u'编译错误'),
            ('Output Limit Exceed', u'超过输出限制'),
            ('Pending', u'等待评测',),
            ('Judging', u'评测中',),
            ('Compiling', u'编译中',),
            ('Rejudging', u'重新评测中',),
            ]

    username = forms.CharField(
            required=False, max_length=30, label=u'用户名',
            widget=forms.TextInput(attrs={'class':'input-medium', 'placeholder':u'用户名'}))
    status = forms.ChoiceField(
            required=False, choices=STATUS, initial='', label=u'结果',
            widget=forms.Select(attrs={'class':'input-medium'}))
    #pid = forms.IntegerField( required=False, label=u'题目编号')
    #cid = forms.IntegerField( required=False, label=u'考试编号')
    #code_length = forms.IntegerField( required=False, label=u'代码长度')

    def __init__(self, idxList, langList, *args, **kwargs):
        super(submissionListForm, self).__init__(*args, **kwargs)
        idxList.insert(0, ('',u'题号'))
        langList.insert(0, ('',u'语言'))
        self.fields['problem_index'] = forms.ChoiceField(
                required=False, choices=idxList,
                initial='', label=u'题号',
                widget=forms.Select(attrs={'class':'input-small'}))
        self.fields['language'] = forms.ChoiceField(
                required=False, choices=langList,
                initial='', label=u'语言',
                widget=forms.Select(attrs={'class':'input-medium'}))

