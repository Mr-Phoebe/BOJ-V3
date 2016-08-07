# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.http import Http404, HttpResponse
from User.models import User
from Submission.models import Submission
from Contest.models import Contest, ContestProblem
from operator import itemgetter, attrgetter
from Course.models import Course, CourseClass
from kari.const import Const
from datetime import *

def index(request):
    return render_to_response('newtpl/index.html', {
        'user':User.getSessionUser(request.session),
        'tpl_sp_page':True,
        'tpl_nav_act':'index',
        })

def mycmp(x, y):
    if x[2] != y[2] :
        return - cmp(x[2], y[2])
    elif x[3] == y[3] :
        return cmp(x[0], y[0])
    else :
        return cmp(x[3], y[3])

def board(request):
    cid = request.GET.get('cid', 1)
    contest = Contest.getById(cid)
    '''
    if contest == False :
        errmsg = u'不存在考试编号为' + str(cid) + u'的考试'
        return render(request, 'error.html', {'errmsg' : errmsg, 'user' : User.getSessionUser(request.session)})
    contestProblem = contest.getContestProblem()
    startTime = contest.start_time
    '''
    submission = Submission.submissionList(cid = cid)
    
    problemIndex = list()
    problemIndex.append('A')#
    problemIndex.append('B')#
    '''
    for i in contestProblem:
        problemIndex.append(i.problem_index)
    '''
    problemIndex.sort()
    
    data = dict()
    cnt = 0
    now = datetime.now()
    now = now - now
    for i in submission :
        if i.user.username not in data :
            data[i.user.username] = [cnt, i.user.username,  0, now] #id, username, solved, time, A, B, etc
            cnt = cnt + 1
            for j in problemIndex :
                data[i.user.username].append({'ac' : 0, 'pd' : 0, 'other' : 0})

        tmp = data[i.user.username]
        tp = tmp[i.problem_index.problem_index + 3]
        if tp['ac'] == 0 :
            if ('Accepted', 'Accepted') in i.status :
                tp['ac'] = 1
                tp['other'] = tp['other'] + 1
                tmp[3] += datetime.timedelta((tp['pd'] + tp['ac'] + tp['other']) * 20) + (i.submission_time - startTime)
                tmp[2] += 1
            elif ('Pending', 'Pending') in i.status :
                tp['pd'] = tp['tp'] + 1
            else :
                tp['other'] = tp['other'] + 1

    out = list()
    for i in data :
        out.append(data[i])
   
    out.append([0, 'zhangzhou', 12, -(datetime.now() - datetime.now()) , {'ac': 0, 'pd' : 2, 'other' : 0}, {'ac' : 0,'pd' : 0, 'other' : 0}])#
    out.append([-1, 'lyy', 12, -(datetime.now() - datetime.now()), {'ac': 1, 'pd' : 2, 'other' : 3}, {'ac': 0, 'pd' : 0, 'other' : 0}])#
    out.sort(cmp = mycmp)
    cnt = 1
    for i in out :
        i[0] = cnt
        cnt = cnt + 1
        i[3] = (datetime(2000, 1, 1, 0, 0, 0, 0) + i[3]).strftime("%H:%M:%S")

    return render(request, 'lyy/board.html', {'out' : out, 'problemIndex' : problemIndex, 'user' : User.getSessionUser(request.session)})

def showStudentByCCId(request) :
    id = request.GET.get('id', 1)
    user = User.getSessionUser(request.session)
    if user == False :
        errmsg = u'请先登录'
        return render(request, 'error.html', {'errmsg' : errmsg, 'user' : user})

    ''' 
    try :
        courseClass = CourseClass.getById(id)
    except Exception as e:
        return render(request, 'error.html', {'errmsg' : e, 'user' : user})

    if courseClass.isAdmin(User) == False :
        errmsg =u'您不是该课程分班的课程分班管理员，无法查看该课程分班的学生'
        return render(request, 'error.html', {'errmsg' : e, 'user' : user})
    
    allStudent = courseClass.getAllStudent()
    '''

    allStudent = []
    allStudent.append(User.objects.get(pk=1))
    allStudent.append(User.objects.get(pk=1))
    return render(request, 'lyy/showStudentByCCId.html', {'allStudent' : allStudent, 'user' : user})

def showCourseClass(request) :
    user = User.getSessionUser(request.session)
    courseClass = list()

    '''
    if user == False :
        errmsg = u'请先登录'
        return render(request, 'error.html', {'errmsg' : e, 'user' : user})
   
    if user.isCourseClassAdmin == True :
        courseClass = CourseClass.getByAdmin(user)
        admin = user
    elif user.isStudent == True :
        courseClass = CourseClass.getByStudent(user)
        student = user
    else :
        errmsg = u'您既不是课程管理员也不是学生，无权限访问该页面'
        return render(request, 'error.html', {'errmsg' : e, 'user' : user})
    '''
    
    return render(request, 'lyy/showCourseClass.html', {'courseClass' : courseClass, 'user' : user})
