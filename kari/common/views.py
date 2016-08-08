# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.http import is_safe_url
from common.utils import referer
from common.err import Err
from common.forms import RegisterForm
from User.models import User, University, Group
import logging

logger = logging.getLogger('django')

def index(request):
    return render(request, 'newtpl/index.html', {
        #'user':User.getSessionUser(request.session),
        'tpl':{
            'nav_act':'index',
            },
        })

def login(request):
    if request.method != 'POST':
        return redirect('/')

    try:
        username = request.POST['username']
        passwd = request.POST['passwd']
        u = User.getUserByRawUsername(username)
        if u!=None and u!=False and u.checkPasswd(passwd):
            request.session['uid'] = u.uid
            return redirect(referer(request))
        else:
            username = 'test#' + username
            u = User.getUserByRawUsername(username)
            if u!=None and u!=False and u.checkPasswd(passwd):
                request.session['uid'] = u.uid
                return redirect(referer(request))
            else:
                raise Exception('login err')
    except Exception as e:
        messages.error(request, u'用户名或密码错误')
        return redirect(referer(request))

def register(request):
    try:
        if request.method != 'POST':
            return render(request, 'newtpl/register.html', {})
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            passwd_1 = form.cleaned_data['passwd1']
            passwd_2 = form.cleaned_data['passwd2']
            if passwd_1 != passwd_2:
                raise Exception(u'两次密码不一致')
            test_uni = University.getByName('test')
            new_user = User.addUser(username, passwd_1, test_uni, 'student')
            group = Group.getById(52)
            group.addMember(new_user)
            messages.add_message(request, messages.SUCCESS, u'注册用户test#%s成功！' % username)
            return redirect("/")
            # return redirect('User:viewuser', uid = new_user.uid)
        else:
            raise Exception('注册失败！')
    except Exception as e:
        logger.error(unicode(e).replace('\n', '\t'))
        messages.error(request, u'输入信息不合法或该用户已被注册！')
        return render(request, Err.ERROR_PAGE)

def logout(request):
    request.session.flush()
    return redirect('/')

def faq(request):
    return render(request, 'newtpl/faq.html', {})

def whitepaper(request):
    return render(request, 'newtpl/whitepaper.html', {})

def about(request):
    return render(request, 'newtpl/about.html', {})

def http403(request):
    return render(request, 'newtpl/403.html', {'err_msg_list':[
        u'您遇到了 <a href="http://zh.wikipedia.org/wiki/HTTP%E7%8A%B6%E6%80%81%E7%A0%81#403">HTTP 403</a> 错误。',
        u'服务器拒绝了您的请求。',
        ]})

def http404(request):
    return render(request, 'newtpl/404.html', {'err_msg_list':[
        u'您遇到了 <a href="http://zh.wikipedia.org/wiki/HTTP%E7%8A%B6%E6%80%81%E7%A0%81#404">HTTP 404</a> 错误。',
        u'该错误通常是由于访问了不存在的URL所导致的。',
        ]})

def http500(request):
    return render(request, 'newtpl/500.html', {'err_msg_list':[
        u'您遇到了 <a href="http://zh.wikipedia.org/wiki/HTTP%E7%8A%B6%E6%80%81%E7%A0%81#500">HTTP 500</a> 错误。',
        u'服务器内部错误，程序异常。',
        ]})

def test(request):
    messages.error(request, '悲剧啦')
    err = ['hehehhee', 'hihihii']
    return render(request, 'newtpl/error.html', {'eee':err})

