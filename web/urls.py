"""cmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from web import views

urlpatterns = [
    url(r'^index/$',views.index),
    url(r'^change_passwd/$',views.change_passwd),
    url(r'^acc_logout/$',views.acc_logout),
    url(r'^project/$',views.pro_manage),
    url(r'^host/$',views.host_manage),
    url(r'^checkProjectInfo/$',views.checkProjectInfo),
    url(r'^checkHostInfo/$',views.checkHostInfo),
    url(r'^update_project/$',views.update_project),
    url(r'^update_host/$',views.update_host),
    url(r'^BatchPublishing/$',views.BatchPublish_code),
    url(r'^SinglePublishing/$',views.SinglePublish_code),
    url(r'^check_result/$',views.check_result),
    url(r'^log/$',views.check_log),
]
