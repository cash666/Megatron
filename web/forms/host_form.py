#coding:utf8
from django import forms
from web import models
from django.core.exceptions import ValidationError
#import re

#def ip_validate(value):
#        ip_re=re.compile(r'^([1-9][0-9]|1[0-9][0-9]|2[0-5][0-4])\.([1-9][0-9]|1[0-9][0-9]|2[0-5][0-4])\.([1-9][0-9]|1[0-9][0-9]|2[0-5][0-4])\.([1-9][0-9]|1[0-9][0-9]|2[0-5][0-4])$')
#        if not ip_re.match(value):
#                        raise forms.ValidationError('IP格式错误')

class HostForm(forms.Form):
	id=forms.CharField(widget=forms.HiddenInput(),required=False)
	hostname=forms.CharField(max_length=10,widget=forms.TextInput(attrs={'class': "form-control",'onblur':'checkHostInfo(this)'}))
	InnerIp=forms.CharField(max_length=64,widget=forms.TextInput(attrs={'class': "form-control",'onblur':'checkHostInfo(this)'}))
        OuterIp=forms.CharField(max_length=64,widget=forms.TextInput(attrs={'class': "form-control",'onblur':'checkHostInfo(this)'}))
	project=forms.CharField(widget=forms.Select(attrs={'class': "form-control",'onblur':'checkHostInfo(this)'}))

	def __init__(self,*args,**kwargs):
                super(HostForm,self).__init__(*args,**kwargs)
                self.fields['project'].widget.choices=models.Project.objects.all().values_list('id','name')
