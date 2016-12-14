#coding:utf8
from django import forms
from web import models

class ProjectForm(forms.Form):
	id=forms.CharField(widget=forms.HiddenInput(),required=False)
	name=forms.CharField(max_length=10,widget=forms.TextInput(attrs={'class': "form-control",'onblur':'checkProjectInfo(this)'}))
	pro_src=forms.CharField(max_length=32,widget=forms.TextInput(attrs={'class': "form-control",'onblur':'checkProjectInfo(this)'}))
	pro_dest=forms.CharField(max_length=32,widget=forms.TextInput(attrs={'class': "form-control",'onblur':'checkProjectInfo(this)'}))
	creater=forms.CharField(max_length=32,required=False,widget=forms.TextInput(attrs={'class': "form-control"}))
	description=forms.CharField(max_length=100,required=False,widget=forms.widgets.Textarea(attrs={'class':'form-control','placeholder':u'项目描述','rows':7}))
