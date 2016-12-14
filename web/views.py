#coding:utf8

from django.shortcuts import render,HttpResponse,redirect,render_to_response,get_object_or_404
from web import models
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from web.forms import project_form,host_form
import re,json,os
import subprocess
from conf import config
from api import result_api
import datetime

# Create your views here.
def check_login():
        def decorator(func):
                def wrapper(request):
                        if request.user.is_authenticated:
                                return func(request)
                        else:
                                return redirect('/')
                return wrapper
        return decorator

def page_not_found(request):
    return render_to_response('404.html')

def page_error(request):
    return render_to_response('500.html')

def acc_login(request):
        message=''
        if request.method == 'POST':
                username=request.POST.get('username')
                password=request.POST.get('password')
                user=authenticate(username=username,password=password)
                if user is not None:
                        login(request,user)
                        return redirect('/megatron/index/')
                else:
                        message=u"用户名或密码错误"
        return render(request,'login.html',{'message':message})

def acc_logout(request):
        logout(request)
        return redirect('/')

#@check_login()
@login_required()
def index(request):
	project_obj=models.Project.objects.all()
	project_count=models.Project.objects.count()
	host_count=models.Host.objects.count()
	today = datetime.date.today()
	series=[]
        date_list=[today - datetime.timedelta(days=6),today - datetime.timedelta(days=5),today - datetime.timedelta(days=4),today - datetime.timedelta(days=3),today - datetime.timedelta(days=2),today - datetime.timedelta(days=1),today]
	for project in project_obj:
		p_name=project.name
		id=project.id
		dic_name='count_dic_%s' % id
		dic_name={}
		dic_name['name']=u'%s代码发布次数统计' % p_name
                dic_name['data']=[]
		for d in date_list:
			count=models.LogInfo.objects.filter(project_name=p_name,public_time__startswith=d).count()
			dic_name['data'].append(count)
		series.append(dic_name)
        json_series=json.dumps(series,separators=(',',':'))
	publish_obj=models.LogInfo.objects.all()[0:6]
	return render(request,'index.html',{'json_series':json_series,'project_count':project_count,'host_count':host_count,'publish_obj':publish_obj})

@login_required(login_url='/')
def change_passwd(request):
	if request.method == 'POST':
		old_passwd=request.POST.get('old_passwd','')
		new_passwd=request.POST.get('new_passwd','')
		new_passwd2=request.POST.get('new_passwd2','')
		if not old_passwd:
			message=u'原来密码不能为空'
			return redirect('/megatron/change_passwd/?message=%s' % message)
		elif not new_passwd:
			message=u'新密码不能为空'
                        return redirect('/megatron/change_passwd/?message=%s' % message)
		elif not new_passwd2:
			message=u'重复密码不能为空'
                        return redirect('/megatron/change_passwd/?message=%s' % message)
		user_obj=User.objects.get(username=request.user.userinfo.user)
		if user_obj.check_password(old_passwd):
			if new_passwd==new_passwd2:
				user_obj.set_password(new_passwd)
				user_obj.save()
				message=u'密码修改成功'
                        	return redirect('/megatron/change_passwd/?message=%s' % message)
			else:
				message=u'两次密码输入不一致'
                                return redirect('/megatron/change_passwd/?message=%s' % message)
		else:
			message=u'原密码输入不正确'
			return redirect('/megatron/change_passwd/?message=%s' % message)
	return render(request,'change_passwd.html')

@login_required(login_url='/')
def pro_manage(request):
	project_list=models.Project.objects.all()
	ProjectForm=project_form.ProjectForm()
	id=request.GET.get('id','')
	if id:
		is_ok=models.Project.objects.filter(id=id).delete()
		if is_ok:
			return HttpResponse('ok')
	if request.method == 'POST':
		ProjectForm=project_form.ProjectForm(request.POST)
		if ProjectForm.is_valid():
			data=ProjectForm.clean()
			is_ok=models.Project.objects.create(name=data['name'],pro_src=data['pro_src'],pro_dest=data['pro_dest'],creater=request.user.userinfo.name,description=data['description'])
			if is_ok:
				message=u'添加项目成功'
			else:
				message=u'添加项目失败'
			return redirect('/megatron/project/?message=%s' % message)
	else:
		return render(request,'project.html',{'project_list':project_list,'ProjectForm':ProjectForm})

@check_login()
def checkProjectInfo(request):
	if request.method == 'POST':
		text=request.POST.get('text','')
		attr_name=request.POST.get('name','')
		if text and attr_name:
			if attr_name == 'name':
				is_exist=models.Project.objects.filter(name=text)
				if is_exist:
					return HttpResponse(u'该项目名称已经存在')
				else:
					return HttpResponse('')
			elif attr_name == 'pro_src':
				is_exist=models.Project.objects.filter(pro_src=text)
				if is_exist:
                                        return HttpResponse(u'该项目源地址已经存在')
				else:
                                        return HttpResponse('')
			elif attr_name == 'pro_dest':
				is_exist=models.Project.objects.filter(pro_dest=text)
				if is_exist:
                                        return HttpResponse(u'该项目目标地址已经存在')
				else:
                                        return HttpResponse('')
			else:
				pass

@check_login()
@permission_required('web.change_project',login_url='/megatron/403.html',raise_exception=True)
def update_project(request):
	id=request.GET.get('id','')
	ProjectForm=project_form.ProjectForm()
	message=''
	if request.method == 'POST':
		ProjectForm=project_form.ProjectForm(request.POST)
                if ProjectForm.is_valid():
			data=ProjectForm.clean()
			try:
                        	models.Project.objects.filter(id=data['id']).update(name=data['name'],pro_src=data['pro_src'],pro_dest=data['pro_dest'])
			except Exception as e:
				message=u'出错了,出错信息为:%s' % e
			else:
				message=u'修改成功'
			finally:
				return redirect('/megatron/project/?message=%s' % message)
	if id:
		project_list=models.Project.objects.get(id=id)
		return render(request,'update_project.html',{'project_list':project_list,'ProjectForm':ProjectForm})

@check_login()
def host_manage(request):
	HostForm=host_form.HostForm()
	host_list=models.Host.objects.all()
	id=request.GET.get('id','')
        if id:
                is_ok=models.Host.objects.filter(id=id).delete()
                if is_ok:
                        return HttpResponse('ok')
	if request.method == 'POST':
		HostForm=host_form.HostForm(request.POST)
                if HostForm.is_valid():
                        data=HostForm.clean()
			is_ok=models.Host.objects.create(hostname=data['hostname'],innerip=data['InnerIp'],outerip=data['OuterIp'],host_id=data['project'])
			if is_ok:
                                message=u'添加主机成功'
                        else:
                                message=u'添加主机失败'
                        return redirect('/megatron/host/?message=%s' % message)
        return render(request,'host.html',{'host_list':host_list,'HostForm':HostForm})

@check_login()
def checkHostInfo(request):
	if request.method == 'POST':
		text=request.POST.get('text','')
                attr_name=request.POST.get('name','')
                if text and attr_name:
                        if attr_name == 'hostname':
                                is_exist=models.Host.objects.filter(hostname=text)
                                if is_exist:
                                        return HttpResponse(u'该主机名已经存在')
                                else:
                                        return HttpResponse('')
                        elif attr_name == 'InnerIp':
				ip_re=re.compile(r'^([1-9][0-9]|1[0-9][0-9]|2[0-5][0-4])\.([1-9][0-9]|1[0-9][0-9]|2[0-5][0-4])\.([1-9][0-9]|1[0-9][0-9]|2[0-5][0-4])\.([1-9][0-9]|1[0-9][0-9]|25[0-4]|2[0-4][0-9])$')
	        		if not ip_re.match(text):
					return HttpResponse(u'内网IP格式出错')
                                is_exist=models.Host.objects.filter(innerip=text)
                                if is_exist:
                                        return HttpResponse(u'该内网IP已经存在')
                                else:
                                        return HttpResponse('')
                        elif attr_name == 'OuterIp':
				ip_re=re.compile(r'^([1-9][0-9]|1[0-9][0-9]|2[0-5][0-4])\.([1-9][0-9]|1[0-9][0-9]|2[0-5][0-4])\.([1-9][0-9]|1[0-9][0-9]|2[0-5][0-4])\.([1-9][0-9]|1[0-9][0-9]|25[0-4]|2[0-4][0-9])$')
                                if not ip_re.match(text):
                                        return HttpResponse(u'外网IP格式出错')
                                is_exist=models.Host.objects.filter(outerip=text)
                                if is_exist:
                                        return HttpResponse(u'该外网IP已经存在')
                                else:
                                        return HttpResponse('')

@check_login()
def update_host(request):
        id=request.GET.get('id','')
        HostForm=host_form.HostForm()
        message=''
        if request.method == 'POST':
                HostForm=host_form.HostForm(request.POST)
                if HostForm.is_valid():
                        data=HostForm.clean()
                        try:
                                models.Host.objects.filter(id=data['id']).update(hostname=data['hostname'],innerip=data['InnerIp'],outerip=data['OuterIp'],host=data['project'])
                        except Exception as e:
                                message=u'出错了,出错信息为:%s' % e
                        else:
                                message=u'修改成功'
                        finally:
                                return redirect('/megatron/host/?message=%s' % message)
        if id:
                host_list=models.Host.objects.get(id=id)
                return render(request,'update_host.html',{'host_list':host_list,'HostForm':HostForm})

@check_login()
def SinglePublish_code(request):
	HostForm=host_form.HostForm()
	if request.method == 'POST':
                ip_list=request.POST.get('ip_list','')
                file_list=request.POST.get('file_list','')
                id=request.POST.get('id','')
                ip_list=json.loads(ip_list.encode('utf8'))
                file_list=json.loads(file_list.encode('utf8'))
                section=config.section
                port=config.port
                username=config.username
                passwd=config.passwd
                pro_obj=models.Project.objects.filter(id=id)
                os.remove('/etc/ansible/hosts')
                f=open('/etc/ansible/hosts','a')
                f.write('[%s]\n' % section)
                if pro_obj:
                        for item in pro_obj:
                                pro_src=item.pro_src
                                pro_dest=item.pro_dest
                                pro_name=item.name
                ret="<div><strong>%s</strong><span><input type='button' class='btn btn-primary pull-right' id='check_result' data-style='slide-down' onclick='CheckResult(this)' value=%s /></span></div>" % (u'传输结果:',u'校验结果')
		all_list=[]
		check_ip_list=[]
                for ip in ip_list:
                        content='%s ansible_ssh_port=%s ansible_ssh_user=%s ansible_ssh_pass=%s\n' % (ip,port,username,passwd)
                        f.write(content)
                f.close()
                models.LogInfo.objects.create(project_name=pro_name,operate_name=request.user.userinfo.name,operate_type=u'单量发布')
		for file in file_list:
                	publish_cmd='rsync_timeout=5 src=%s/%s dest_port=%s dest=%s' % (pro_src,file,port,pro_dest)
                	result_list=result_api.get_result('synchronize',publish_cmd,section,file)
			all_list.append(result_list)
		if all_list:
                	for result_list in all_list:
                        	for ip,res in result_list.iteritems():
					if ip not in check_ip_list:
						check_ip_list.append(ip)
                                		if res['status'] == 'ok':
                                        		ret2="<div style='color:green;border-bottom:1px solid green'>%s------%s</div>" % (ip,u'成功')
                                        		ret+=ret2
                                		elif res['status'] == 'fail':
                                        		ret2="<div style='color:red;border-bottom:1px solid red'>%s------%s</div>" % (ip,u'文件[%s]上传失败:%s' % (res['upload_file'],res['result'].split('\n')[0]))
                                        		ret+=ret2
					else:
						if res['status'] == 'fail':
							ret2="<div style='color:red;border-bottom:1px solid red'>%s------%s</div>" % (ip,u'文件[%s]上传失败:%s' % (res['upload_file'],res['result'].split('\n')[0]))
                                                        ret+=ret2
                return HttpResponse(mark_safe(ret))
        id=request.GET.get('id','')
        if id:
                host_html="<div><input type='button' value=%s onclick='SelectAll()' class='btn btn-success'/>&nbsp;<input type='button' value=%s class='btn btn-success' onclick='Reverse()' />&nbsp;<input type='button' class='btn btn-success' value=%s onclick='Cancel()' /><input type='button' class='btn btn-danger ladda-button pull-right' onclick='PublishCode(this)' data-style='slide-down' value='%s' id='publish_btn' /></div>" % (u'全选',u'反选',u'取消',u'发布代码')
                host_html+='<div id="select_list"><div>'
                count=0
                host_list=models.Host.objects.filter(host_id=id)
                for item in host_list:
                        count+=1
                        if count%9==0:
                                host_html+='</div><div>';
                        else:
                                host_html+='<input type="checkbox" value=%s>%s&nbsp;' % (item.outerip,item.outerip)
                host_html+='</div>'
		pro_obj=models.Project.objects.get(id=id)
		pro_src=pro_obj.pro_src
		file_list=os.listdir(pro_src)
		count2=0
		file_html="<div id='file_list'><div>"
		for item in file_list:
			count2+=1
			if count2%12==0:
				file_html+='</div><div>';
			else:
				file_html+='<input type="checkbox" value=%s>%s&nbsp;' % (item,item)
		file_html+='</div>'
		list_html=[file_html,host_html]
		json_html=json.dumps(list_html)
                return HttpResponse(json_html)
	return render(request,'SinglePublishing.html',{'HostForm':HostForm})	

@check_login()
def BatchPublish_code(request):
	HostForm=host_form.HostForm()
	if request.method == 'POST':
		ip_list=request.POST.get('ip_list','')
		id=request.POST.get('id','')
		ip_list=json.loads(ip_list.encode('utf8'))
		section=config.section
		port=config.port
		username=config.username
		passwd=config.passwd
		pro_obj=models.Project.objects.filter(id=id)
		os.remove('/etc/ansible/hosts')
                f=open('/etc/ansible/hosts','a')
                f.write('[%s]\n' % section)
		if pro_obj:
			for item in pro_obj:
				pro_src=item.pro_src
				pro_dest=item.pro_dest
				pro_name=item.name
		ret="<div><strong>%s</strong><span><input type='button' class='btn btn-primary pull-right' id='check_result' data-style='slide-down' onclick='CheckResult(this)' value=%s /></span></div>" % (u'传输结果:',u'校验结果')
		fail_list=[]
		for ip in ip_list:
			content='%s ansible_ssh_port=%s ansible_ssh_user=%s ansible_ssh_pass=%s\n' % (ip,port,username,passwd)
                        f.write(content)
		f.close()
		models.LogInfo.objects.create(project_name=pro_name,operate_name=request.user.userinfo.name,operate_type=u'批量发布')
		publish_cmd='rsync_timeout=5 src=%s dest_port=%s dest=%s' % (pro_src,port,pro_dest)
		result_list=result_api.get_result('synchronize',publish_cmd,section)
		if result_list:
			for ip,res in result_list.iteritems():
				if res['status'] == 'ok':
					ret2="<div style='color:green;border-bottom:1px solid green'>%s------%s</div>" % (ip,u'成功')
					ret+=ret2
				elif res['status'] == 'fail':
					ret2="<div style='color:red;border-bottom:1px solid red'>%s------%s</div>" % (ip,u'失败:%s' % res['result'].split('\n')[0])
					fail_list.append(ip)
                        		ret+=ret2
		if len(fail_list)!=0:
			ret+=u'<div>本次共上传%d台服务器,失败个数为:%d,失败的IP为:%s</div>' % (int(len(ip_list)),int(len(fail_list)),','.join(fail_list))
		else:
			
			ret+=u'<div>本次共上传%d台服务器,全部成功!' % (int(len(ip_list)))
		return HttpResponse(mark_safe(ret))
	id=request.GET.get('id','')
	if id:
		host_html="<div><input type='button' value=%s onclick='SelectAll()' class='btn btn-success'/>&nbsp;<input type='button' value=%s class='btn btn-success' onclick='Reverse()' />&nbsp;<input type='button' class='btn btn-success' value=%s onclick='Cancel()' /><input type='button' class='btn btn-danger ladda-button pull-right' onclick='PublishCode(this)' data-style='slide-down' value='%s' id='publish_btn' /></div>" % (u'全选',u'反选',u'取消',u'发布代码')
		host_html+='<div id="select_list"><div>'
		count=0
		host_list=models.Host.objects.filter(host_id=id)
		for item in host_list:
			count+=1
			if count%9==0:
				host_html+='</div><div>';
			else:
				host_html+='<input type="checkbox" value=%s>%s&nbsp;' % (item.outerip,item.outerip)
		host_html+='</div>'
		return HttpResponse(mark_safe(host_html))
	return render(request,'BatchPublishing.html',{'HostForm':HostForm})

@check_login()
def check_result(request):
	if request.method == 'POST':
                ip_list=request.POST.get('ip_list','')
		file_list=request.POST.get('file_list','')
                id=request.POST.get('id','')
                ip_list=json.loads(ip_list.encode('utf8'))
		section=config.section
		pro_obj=models.Project.objects.filter(id=id)
		ret='<div><strong>%s</strong></div>' % (u'校验结果如下:')
		file_ret='<div><strong>%s</strong></div>' % (u'各文件校验结果如下:')
		all_list={}
                if pro_obj:
                        for item in pro_obj:
                                pro_src=item.pro_src
                                pro_dest=item.pro_dest
		if file_list:
                        file_list=json.loads(file_list.encode('utf8'))
			for file in file_list:
				cmd='md5sum %s%s' % (pro_dest,file)
				result_list=result_api.get_result('shell',cmd,section)
				all_list[file]=result_list
			if all_list:
				for file,result_list in all_list.iteritems():
					file_ret+='<div><strong>%s%s</strong></div>' % (file,u'的校验结果如下:')
                        		for ip,res in result_list.iteritems():
                                		if res['status'] == 'ok':
                                        		file_ret2="<div style='color:green;border-bottom:1px solid green'>%s------%s</div>" % (ip,res['result'].split()[0])
                                        		file_ret+=file_ret2
                                		elif res['status'] == 'fail':
                                        		file_ret2="<div style='color:red;border-bottom:1px solid red'>%s------%s</div>" % (ip,u'获取失败:%s' % res['result'].split('\n')[0])
                                        		file_ret+=file_ret2
			for file in file_list:
				file_md5=os.popen('md5sum %s%s' % (pro_src,file)).read()
				file_md5=file_md5.split()[0]	
				file_ret+='------------------------------------------------------------------'
				file_ret+='<div><strong>%s:%s</strong></div>' % (file,file_md5)
			return HttpResponse(mark_safe(file_ret))
			
		cmd='cat %sversion.txt' % pro_dest
		result_list=result_api.get_result('shell',cmd,section)
		if result_list:
			for ip,res in result_list.iteritems():
				if res['status'] == 'ok':
					ret2="<div style='color:green;border-bottom:1px solid green'>%s------%s</div>" % (ip,res['result'])
                                	ret+=ret2
				elif res['status'] == 'fail':
					ret2="<div style='color:red;border-bottom:1px solid red'>%s------%s</div>" % (ip,u'获取失败:%s' % res['result'].split('\n')[0])
                                	ret+=ret2
		if os.popen('cat %sversion.txt' % pro_src).read():
			version=os.popen('cat %sversion.txt' % pro_src).read()
		else:
			version=u'没有发现版本文件'
		ret+='<div><strong>%s:%s</strong></div>' % (u'本次更新的代码的版本是',version)
		return HttpResponse(mark_safe(ret))

@check_login()
def check_log(request):
	log_obj=models.LogInfo.objects.all()
	return render(request,'log.html',{'log_obj':log_obj})
