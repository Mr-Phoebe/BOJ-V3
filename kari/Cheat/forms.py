# -*- coding: utf-8 -*-
from django import forms

class ChooseProbForm(forms.Form):
    def __init__(self, cp, *args, **kwargs):
        super(ChooseProbForm, self).__init__(*args, **kwargs)
        self.fields['contest_problem'] = forms.ModelMultipleChoiceField(
                label=u'题目选择',
                queryset = cp,
                widget = forms.CheckboxSelectMultiple,
                )
