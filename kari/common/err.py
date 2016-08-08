#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import messages
from kari.const import Const

class Err(Exception):

    ERROR_PAGE = 'newtpl/error.html'

    #日志错误等级
    LOG_LEVEL = {
            'success':0,
            'critical':10,
            'error':20,
            'warning':30,
            'info':40,
            'debug':50,
    }

    #用户错误等级
    USER_LEVEL = {
        'success': messages.SUCCESS,
        'error': messages.ERROR,
        'warning': messages.WARNING,
        'info': messages.INFO,
        'debug': messages.DEBUG,
    }

    #错误列表
    ERR = {
        #common error
        'unknown err':('error', 'unknown failure occured', 'error', u'未知错误！'),
        'no priv':('info', 'no privilege', 'error', u'您没有该操作的权限'),
        'no resource':('error', 'no resource', 'error', u'您所请求的资源不存在！'),
        
        #user
        'not login':('info', 'not login', 'info', u'请先登录！'),
        'login err':('info', 'login err', 'error', u'用户名或密码错误！'),
        'logged in':('info', 'logged in', 'error', u'您已经登陆过了！'),
        'not pvlg':('info', 'not pvlg', 'error', u'您没有足够的权限！'),
        'update error':('error', 'update error', 'error', u'您提供的信息有如下问题：%s'),
        'passwd diff':('error', 'passwd diff', 'error', u'两次密码不一致！'),
        'username dup':('error', 'username dup', 'error', u'用户名已存在！'),
        'username illegal':('error', 'username illegal', 'error', u'用户名非法！用户名长度应在%d到%d之间且仅包含a-z,0-9,_'%(Const.USERNAME_MIN_LENGTH, Const.USERNAME_MAX_LENGTH)),
        'email illegal':('error', 'email illegal', 'error', u'Email地址非法！'),
        'passwd illegal':('error', 'passwd illegal', 'error', u'密码非法！密码长度应在%d到%d之间。'%(Const.PASSWD_MIN_LENGTH, Const.PASSWD_MAX_LENGTH)),
        'school not exist':('error', 'school not exist', 'error', u'学院不存在！'),
        'school info illegal':('error', 'school info illegal', 'error', u'太长啦'),
        'schoolname illegal':('error', 'schoolname illegal', 'error', u'非法的学校名称！'),
        'schoolabbr illegal':('error', 'schoolabbr illegal', 'error', u'非法的学校简称！'),
        'groupname illegal':('error', 'groupname illegal', 'error', u'群组名称非法！名称长度应在%d到%d之间。'%(Const.GROUPNAME_MIN_LENGTH, Const.GROUPNAME_MAX_LENGTH)),
        'group not exist':('error', 'group not exist', 'error', u'分班不存在！'),
        'no such user':('error', 'no such user', 'error', u'指定的用户不存在！'),
        
        #problem
        'problem illegal':('info', 'no such problem', 'error', u'题目不存在'),
        'problem info illegal':('info', 'problem info illegal', 'error', u'题目信息非法'),
        'no problem priv':('info', 'no problem priv', 'error', u'您没有使用该题目的权限'),
        'testdata illegal':('info', 'no such testdata', 'error', u'测试数据不存在'),
        'testdata mode illegal':('info', 'testdata mode illegal', 'error', u'输入/输出文件非法'),

        #contest
        'contest not started':('info', 'contest not started', 'error', u'考试尚未开始！'),

        #example
        'example err':('info', 'str1 %s str2 %s', 'info', u'呵呵1 %s 呵呵2 %s'),
        'request err':('info', 'url %s http request %s error', 'info', u' %s %s'),
        #course
        'no contest':('info', 'no such contest %s; %s', 'info', u'没有编号为%s的考试，以及%s'),
        'no contestproblem':('info', 'no such contestproblem %s; %s', 'info', u'没有名为%s的题目，以及%s'),
        'no problem':('info', 'no such problem %s; %s', 'info', u'没有名为%s的题目，以及%s'),
        'no courseclass':('info', 'no such courseclass %s; %s', 'info', u'没有编号为%s的分班，以及%s'),
        'no course':('info', 'no such course %s; %s', 'info', u'没有编号为%s的课程，以及%s'),
        'no school':('info', 'no such school %s; %s', 'info', u'没有编号为%s的学院，以及%s'),
        'no group':('info', 'no such group %s; %s', 'info', u'没有编号为%s的班级，以及%s'),
        'no submission':('info', 'no such submission %s; %s', 'info', u'没有编号为%s的提交，以及%s'),
        'no generalsubmission':('info', 'no such general_submission %s; %s', 'info', u'没有编号为%s的提交，以及%s'),
        #submission
        'illegal language':('info', 'the submitted language %s not listed in the allowed language list; %s', 'info', u'您选择的语言%s不在允许提交的语言列表之内，以及%s'),
        'submit err':('info', 'err: %s reason: %s', 'info', u'错误: %s 原因: %s'),
    }

    def __init__(self, request, err='unknown err', log_format=(), user_format=(), *args, **kwargs):
        super(Err, self).__init__(*args, **kwargs)
        try:
            self.e = self.ERR[err]
            self.log_msg = self.e[1] % log_format
            self.user_msg = self.e[3] % user_format
        except:
            self.e = self.ERR['unknown err']
            self.log_msg = self.e[1]
            self.user_msg = self.e[3]
        messages.add_message(request, self.USER_LEVEL[self.e[2]], self.user_msg)

    def __unicode__(self):
        return self.log_msg

