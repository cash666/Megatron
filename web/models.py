#coding:utf8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
	'''
	项目表
	'''
	name=models.CharField(max_length=64, verbose_name=u'项目名称',unique=True)
	pro_src=models.CharField(max_length=32, verbose_name=u'项目源地址',unique=True)
	pro_dest=models.CharField(max_length=32, verbose_name=u'项目目标地址',unique=True)
	creater=models.CharField(max_length=32,verbose_name=u'创建人')
	description=models.TextField(null=True,blank=True)
	create_time=models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name

	class Meta:
                verbose_name = u'项目表'
                verbose_name_plural = u'项目表'
		db_table='project'
                ordering=['-create_time']
		
class Host(models.Model):
	'''
	主机表
	'''
	hostname=models.CharField(max_length=32, verbose_name=u'主机名',unique=True)
	innerip=models.CharField(max_length=32,unique=True)
	outerip=models.CharField(max_length=32,unique=True)
	host=models.ForeignKey(Project)
	create_time=models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
                return self.hostname

        class Meta:
                verbose_name = u'主机表'
                verbose_name_plural = u'主机表'
                db_table='host'
                ordering=['-create_time']

class UserInfo(models.Model):
	'''
	账户信息
	'''
        user=models.OneToOneField(User)
        name=models.CharField(max_length=32)

        def __unicode__(self):
                return self.name

        class Meta:
                verbose_name=u'账户信息'
                verbose_name_plural=u'账户信息'
		db_table='userinfo'

class LogInfo(models.Model):
	'''
	操作日志
	'''
	project_name=models.CharField(max_length=32)
	operate_name=models.CharField(max_length=32)
	operate_type=models.CharField(max_length=32,verbose_name=u'操作类型')
	public_time=models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name=u'操作日志表'
                verbose_name_plural=u'操作日志表'
		db_table='loginfo'
		ordering=['-public_time']
