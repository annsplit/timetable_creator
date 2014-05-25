__author__ = 'annsplit'
# -*- coding: utf-8 -*-

from django import forms
from models import report, section_type, reports_time
from django.forms.models import modelformset_factory
from django.utils.translation import ugettext_lazy as _

class ReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        #self.fields['RName'].widget.attrs['style'] = 'width:400px'
        self.fields['RName'].widget.attrs['class'] = 'reportForm'
        self.fields['Reporter'].widget.attrs['class'] = 'reportForm'
        self.fields['Topic'].widget.attrs['class'] = 'reportForm'

    class Meta:
        model = report
        fields = ("RName", "Reporter", "Topic")
        labels = {
            "RName": _(u"Название доклада"),
            "Reporter": _(u"Докладчик"),
            "Topic": _(u"Тематика")
        }

class TypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TypeForm, self).__init__(*args, **kwargs)
        self.fields['TName'].widget.attrs['class'] = 'reportForm'
        self.fields['time_default'].widget.attrs['class'] = 'reportForm'

    class Meta:
        model = section_type
        fields = ("TName", "time_default")
        labels = {
            "TName": _(u"Тип секции"),
            "time_default": _(u"Продолжительность по умолчанию")
        }
#PostFormSet = modelformset_factory(Post, form=PostForm)


class RepTimeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RepTimeForm, self).__init__(*args, **kwargs)
        self.fields['plenary'].widget.attrs['class'] = 'reportForm'
        self.fields['sectional'].widget.attrs['class'] = 'reportForm'
    class Meta:
        model = reports_time
        fields = ("plenary", "sectional")
        labels = {
            "plenary": _(u"Пленарные доклады"),
            "sectional": _(u"Секционные доклады")
        }

ReportFormset = modelformset_factory(report, form=ReportForm, extra=0)
TypeFormset = modelformset_factory(section_type, form=TypeForm, extra=0)

class LoginForm(forms.Form):
    username = forms.CharField(label=u'name')
    password = forms.CharField(label=u'pass', widget=forms.PasswordInput())