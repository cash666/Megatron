#!/usr/bin/env python
# coding=utf-8

import ansible.runner

def get_result(module,cmd,ip,file=None):
	results = ansible.runner.Runner(
       		module_name=module,
       		module_args=cmd,
		timeout=10,
       		pattern=ip,
       		forks=10
	).run()
	result_list={}
	if not results['contacted'] and not results['dark']:
   		return
	for (hostname, result) in results['contacted'].items():
    		if not 'failed' in result:
			result_list[hostname]={}
			if result.get('stdout'):
				result_list[hostname]['status']='ok'
				result_list[hostname]['result']=result['stdout']
			elif result.get('stderr'):
				result_list[hostname]['status']='fail'
                                result_list[hostname]['result']=result['stderr']
				if file:
					result_list[hostname]['upload_file']=file	
			else:
				result_list[hostname]['status']='ok'
		else:
			result_list[hostname]={}
			result_list[hostname]['status']='fail'
			result_list[hostname]['result']=result['msg']
			if file:
				result_list[hostname]['upload_file']=file
	for (hostname, result) in results['dark'].items():
    		if hostname:
			result_list[hostname]={}
			result_list[hostname]['status']='fail'
			result_list[hostname]['result']=result['msg']
			if file:
                        	result_list[hostname]['upload_file']=file
	return result_list
