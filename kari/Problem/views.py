# -.- encoding: utf-8 -.-

from django.http import HttpResponse
from django.shortcuts import render_to_response, render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.core.paginator import Paginator

from django.contrib import messages

from Problem.models import Problem
from Problem.forms import addProblemForm
from common.utils import queryString
from common.err import Err
from User.models import User
from Contest.models import ContestProblem, Contest
from Submission.models import GeneralSubmission
from Statistic.utils import getContestResult, getContestUserResult
from Course.models import Course
from kari.const import Const

from hashlib import md5
from datetime import datetime
import os
import json
import logging

logger = logging.getLogger('django')

def listProblem(request, pageId="1"): # modified
    logger.info(str(request).replace("\n","\t"))
    try:
        pageId = int(pageId)
        u = User.getSessionUser(request.session)
        if not u:
            raise Err(request, 'not login')

        tres = Problem.problemList(u)
        if (pageId-1)*Const.PROBLEM_PER_PAGE>=len(tres):
            raise Err(request, 'unknown err')
        res = tres[(pageId-1)*Const.PROBLEM_PER_PAGE:pageId*Const.PROBLEM_PER_PAGE]
        res = tres
        probs = []
        for p in res:
            all_submits = GeneralSubmission.objects.filter(problem = p)
            all_accepts = all_submits.filter(status = 'Accepted')
            submits = all_submits.count()
            accepts = all_accepts.count()
            ratio = 0 if submits == 0 else 100 * accepts / submits
            probs.append({'accepts': accepts, 'submits': submits, 'ratio': ratio, 'prob': p})
        paginator = Paginator(probs, Const.PROBLEM_PER_PAGE)
        pageId = min(max(int(pageId), 1), paginator.num_pages)
        #return render(request,"newtpl/problem/problemList.html",{'tpl':{'sp':False}, 'problems': probs})
        return render(request,"newtpl/problem/problemList.html",{'tpl':{'sp':False}, 'problems': paginator.page(pageId)})
    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)

def listManageProblem(request, pageId="1"): # modified
    logger.info(str(request).replace("\n","\t"))
    try:
        pageId = int(pageId)
        u = User.getSessionUser(request.session)
        if not u:
            raise Err(request, 'not login')
        if u.priv == 'student':
            raise Err(request, 'no priv')

        problemList = Problem.problemManageList(u)
        """
        tres = Problem.problemList(u)
        if (pageId-1)*Const.PROBLEM_PER_PAGE>=len(tres):
            raise Err(request, 'unknown err')
        res = tres[(pageId-1)*Const.PROBLEM_PER_PAGE:Const.PROBLEM_PER_PAGE]
        """
        info = {}
        if u.university.isAdmin(u):
            info['admin'] = True
        return render(request,"newtpl/problem/manageProblemList.html",{'problem_list': problemList, 'info': info, 'tpl':{'sp':True}})
    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE, {'errmsg': unicode(e)})


def showProblem(request,p_id): # modified
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Err(request, 'not login')
        p_id = int(p_id)
        p = Problem.getById(p_id)
        if not p.canViewProblem(u):
            raise Err(request, 'no priv')
        p.desc=json.loads(p.prob_desc)
        return render(request, "newtpl/problem/showProblem.html", { 'p':p, 'tpl':{'sp':True}})
    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)

def showContestProblem(request,c_id,idx): # modified
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Err(request, 'not login')

        c_id = int(c_id)
        c = Contest.getById(c_id)
    	cn = c.getContestNotice()
        cp = ContestProblem.getBy(c=c, idx=idx)

        try:
            c.canEnterContest(u)
        except:
            raise Err(request, 'no priv')

        can_manage = True
        try:
            c.canBeManaged(u)
        except:
            can_manage = False

        if (not c.canEnterWithTime(u)) and (not can_manage):
            raise Err(request, 'contest not started')

        c.course_class_name = unicode(c.course_class.getFullName())

        p = cp.problem
        p.idx = cp.problem_index
        p.title = unicode(cp.problem_title)
        p.desc=json.loads(p.prob_desc)

        cp_list = c.getContestProblem()       
	for cp, cp_res, cp_user_res in zip(cp_list, getContestResult(c=c), getContestUserResult(c=c, u=u)):
            cp.ac = cp_res['ac_cnt']
            cp.sub = cp_res['sub_cnt']
            cp.user_res = cp_user_res

        return render(request, "newtpl/problem/showContestProblem.html", {'c':c, 'cp_list':cp_list,'contest_notice_list':cn, 'p':p, 'status_query':queryString(problem_index=p.idx), 'tpl':{'sp':True, 'can_manage':can_manage}}) 
    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)

def chooseCourse(request):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Err(request, 'not login')
        if u.isStudent():
            raise Err(request, 'no priv')
        cs_list = Course.getAllManagedCourses(u)

        return render(request,'newtpl/problem/chooseCourse.html',{'list': cs_list, 'tpl':{'sp':True}})
    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)

def deleteProblem(request, problem_id):
    logger.info(str(request).replace("\n","\t"))
    try:
        user = User.getSessionUser(request.session)
        if not user:
            raise Err(request, 'not login')
        try:
            prob = Problem.getById(int(problem_id))
        except:
            raise Err(request, 'problem illegal')
        if not prob.author.university.isAdmin(user):
            raise Err(request, 'no priv')
        prob.deleteProblem()

        messages.add_message(request, messages.SUCCESS, u'删除题目%d成功' % int(problem_id))
        return redirect('Problem:manage')

    except Exception as e:
        return render(request, Err.ERROR_PAGE, {'errmsg': unicode(e)})

def addProblem(request, course_id): # modified
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Err(request, 'not login')
        if course_id == None:
            return redirect('/problem/addProblem/')
        try:
            course_id = int(course_id)
            cs = Course.getById(course_id)
        except:
            raise Exception(u'课程号非法')

        if not Problem.canAddCourseProblem(cs, u):
            raise Err(request, 'no priv')

        if request.method == 'POST':
            form = addProblemForm(request.POST)
            if form.is_valid():
                prb = Problem.addProblem(u.uid,
                        form.cleaned_data['prob_priv'],
                        form.cleaned_data['prob_title'],
                        form.cleaned_data['prob_time'],
                        form.cleaned_data['prob_memory'],
                        form.cleaned_data['prob_codelength'],
                        form.cleaned_data['prob_desc'],
                        form.cleaned_data['is_spj'],
                        0, course_id, "")

                data_count=0
                case_info=""
                if form.cleaned_data['change_data'] == "1":
                    dataInList=request.FILES.getlist('data_in')
                    dataOutList=request.FILES.getlist('data_out')
                    dataScrList=request.POST.getlist('data_scr')
                    if len(dataInList)!=len(dataOutList) or len(dataInList)!=len(dataScrList):
                        raise Exception(u'上传文件有误')
                    for idx, nowData in enumerate(dataInList):
                        path = Const.PROBLEM_DATA_PATH+str(prb.pid)+"/"+str(idx)+".in"
                        if default_storage.exists(path):
                            default_storage.delete(path)
                        default_storage.save(path, nowData)
                    for idx, nowData in enumerate(dataOutList):
                        path = Const.PROBLEM_DATA_PATH+str(prb.pid)+"/"+str(idx)+".out"
                        if default_storage.exists(path):
                            default_storage.delete(path)
                        default_storage.save(path, nowData)
                    dict={}
                    for idx, nowScr in enumerate(dataScrList):
                        dict[str(idx)]=nowScr
                    case_info=json.dumps(dict)

                    data_count=len(dataInList)

                dict={}
                dict['desc']=form.cleaned_data['prob_desc']
                dict['input_desc']=form.cleaned_data['prob_input_desc']
                dict['output_desc']=form.cleaned_data['prob_output_desc']
                dict['input_sample']=form.cleaned_data['prob_input_sample']
                dict['output_sample']=form.cleaned_data['prob_output_sample']
                prob_desc=json.dumps(dict)

                prb.updateProblem(u.uid,
                        form.cleaned_data['prob_priv'],
                        form.cleaned_data['prob_title'],
                        form.cleaned_data['prob_time'],
                        form.cleaned_data['prob_memory'],
                        form.cleaned_data['prob_codelength'],
                        prob_desc,
                        form.cleaned_data['is_spj'],
                        data_count, course_id, case_info)

                return redirect("/problem/p/"+str(prb.pid)+"/")
            else:
                raise Err(request, 'problem info illegal')
        else:
            form = addProblemForm()
            return render(request,'newtpl/problem/modifyProblem.html',{'form': form,'course': cs, 'tpl':{'sp':True}})
    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)

def addProblemSubmit(request):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Err(request, 'not login')
        p = request.POST
        if request.method == 'POST':
            form = addProblemForm(request.POST)
        if not form.is_valid():
            raise Exception(u'数据输入有误')
        course_id = int(p['course_id'])
        if course_id == None:
            raise Exception(u'课程非法')
        cs = Course.getById(course_id)
        if not cs:
            raise Exception(u'课程号非法')
        if not Problem.canAddCourseProblem(cs, u):
            raise Err(request, 'no priv')

        prb = Problem.addProblem(u.uid, p['prob_priv'], p['prob_title'], p['prob_time'],
                p['prob_memory'], p['prob_codelength'], p['prob_desc'], p['is_spj'],
                0, p['course_id'], "")

        data_count=0
        case_info=""

        #If file not exist, Create an empty file.
        open(Const.PROBLEM_DATA_PATH+str(prb.pid)+"/"+"0.in", 'a').close()
        open(Const.PROBLEM_DATA_PATH+str(prb.pid)+"/"+"0.out", 'a').close()

        if p['change_data'] == "1":
            dataInList=request.FILES.getlist('data_in')
            dataOutList=request.FILES.getlist('data_out')
            dataScrList=request.POST.getlist('data_scr')
            if len(dataInList)!=len(dataOutList) or len(dataInList)!=len(dataScrList):
                raise Exception(u'上传文件有误')
            for idx, nowData in enumerate(dataInList):
                path = Const.PROBLEM_DATA_PATH+str(prb.pid)+"/"+str(idx)+".in"
                if default_storage.exists(path):
                    default_storage.delete(path)
                default_storage.save(path, nowData)
            for idx, nowData in enumerate(dataOutList):
                path = Const.PROBLEM_DATA_PATH+str(prb.pid)+"/"+str(idx)+".out"
                if default_storage.exists(path):
                    default_storage.delete(path)
                default_storage.save(path, nowData)
            dict={}
            for idx, nowScr in enumerate(dataScrList):
                dict[str(idx)]=nowScr
            case_info=json.dumps(dict)

            data_count=len(dataInList)

        dict={}
        dict['desc']=p['prob_desc']
        dict['input_desc']=p['prob_input_desc']
        dict['output_desc']=p['prob_output_desc']
        dict['input_sample']=p['prob_input_sample']
        dict['output_sample']=p['prob_output_sample']
        prob_desc=json.dumps(dict)

        prb.updateProblem(u.uid, p['prob_priv'], p['prob_title'], p['prob_time'],
            p['prob_memory'], p['prob_codelength'], prob_desc, p['is_spj'],
            data_count, p['course_id'], case_info)

        return redirect("/problem/p/"+str(prb.pid)+"/")
    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE, {'errmsg': unicode(e)})

def updateProblem(request, p_id):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Err(request, 'not login')
        try:
            p_id = int(p_id)
            p = Problem.getById(p_id)
        except:
            logger.error(str(e).replace("\n","\t"))
            raise Err(request, 'unknown err')

        if not p.canManageProblem(u):
            raise Err(request, 'no priv')

        if request.method == 'POST':
            form = addProblemForm(request.POST)
            if form.is_valid():
                data_count=p.data_count
                case_info=p.case_info

                if form.cleaned_data['change_data'] == "1":
                    dataInList=request.FILES.getlist('data_in')
                    dataOutList=request.FILES.getlist('data_out')
                    dataScrList=request.POST.getlist('data_scr')
                    if len(dataInList)!=len(dataOutList) or len(dataInList)!=len(dataScrList):
                        raise Err(request, 'unknown err')
                    for idx, nowData in enumerate(dataInList):
                        path = Const.PROBLEM_DATA_PATH+str(p.pid)+"/"+str(idx)+".in"
                        if default_storage.exists(path):
                            default_storage.delete(path)
                        default_storage.save(path, nowData)
                    for idx, nowData in enumerate(dataOutList):
                        path = Const.PROBLEM_DATA_PATH+str(p.pid)+"/"+str(idx)+".out"
                        if default_storage.exists(path):
                            default_storage.delete(path)
                        default_storage.save(path, nowData)

                    dict={}
                    for idx, nowScr in enumerate(dataScrList):
                        dict[str(idx)]=nowScr
                    case_info=json.dumps(dict)

                    data_count=len(dataInList)

                dict={}
                dict['desc']=form.cleaned_data['prob_desc']
                dict['input_desc']=form.cleaned_data['prob_input_desc']
                dict['output_desc']=form.cleaned_data['prob_output_desc']
                dict['input_sample']=form.cleaned_data['prob_input_sample']
                dict['output_sample']=form.cleaned_data['prob_output_sample']
                prob_desc=json.dumps(dict)

                p.updateProblem(u.uid,
                        form.cleaned_data['prob_priv'],
                        form.cleaned_data['prob_title'],
                        form.cleaned_data['prob_time'],
                        form.cleaned_data['prob_memory'],
                        form.cleaned_data['prob_codelength'],
                        prob_desc,
                        form.cleaned_data['is_spj'],
                        data_count, p.course_id, case_info)

                return redirect("/problem/p/"+str(p.pid)+"/")
            else:
                raise Err(request, 'unknown err')
        else:
            desc=json.loads(p.prob_desc)
            form = addProblemForm(
                    initial={
                        'prob_title': p.prob_title,
                        'prob_priv': p.prob_priv,
                        'prob_time': p.prob_time,
                        'prob_memory': p.prob_memory,
                        'prob_codelength': p.prob_codelength,
                        'prob_desc': desc['desc'],
                        'prob_input_desc': desc['input_desc'],
                        'prob_output_desc': desc['output_desc'],
                        'prob_input_sample': desc['input_sample'],
                        'prob_output_sample': desc['output_sample'],
                        'is_spj': p.is_spj,
                        'change_data': 0
                        }
                    )
            cases = range(p.data_count)
            return render(request,'newtpl/problem/modifyProblem.html',{'problem':p, 'form': form,'tpl':{'sp':True}, 'update':True, 'cases': cases})
    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)

def previewTestData(request, problem_id, case_id, mode): # mode = 0: view input  mode = 1: view output
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Err(request, 'not login')
        if not problem_id:
            raise Err(request, 'problem illegal')

        try:
            p = Problem.getById(int(problem_id))
        except:
            raise Err(request, 'problem illegal')

        if not p.canManageProblem(u):
            raise Err(request, 'no priv')

        case_id = int(case_id)
        if case_id >= p.data_count:     # [0, data_count)
            raise Err(request, 'testdata illegal')

        mode = int(mode)
        if mode != 0 and mode != 1:
            raise Err(request, 'testdata mode illegal')

        data_preview = p.generateTestDataPreview(case_id, mode)
        return render(request, 'newtpl/problem/previewTestData.html', {'data_preview': data_preview})

    except Exception as e:
        logger.error(str(e).replace('\n','\t'))
        return render(request, Err.ERROR_PAGE)

"""
def deleteTestData(request, problem_id, case_id):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Err(request, 'not login')
        if not problem_id:
            raise Err(request, 'problem illegal')

        try:
            p = Problem.getById(int(problem_id))
        except:
            raise Err(request, 'problem illegal')

        if not p.canManageProblem(u):
            raise Err(request, 'no priv')

        case_id = int(case_id)
        if case_id >= p.data_count:               # [0, data_count)
            raise Err(request, 'testdata illegal')

        data_preview = p.generateTestDataPreview(case_id, mode)
        return render(request, 'newtpl/problem/previewTestData.html', {'data_preview': data_preview})

    except Exception as e:
        logger.error(str(e).replace('\n','\t'))
        return render(request, Err.ERROR_PAGE)
"""

def updateProblemSubmit(request, p_id):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Err(request, 'not login')
        if not p_id:
            raise Exception(u'题号错误')
        p_id = int(p_id)
        ep = Problem.getById(p_id)
        if not ep:
            raise Exception(u'题号错误')
        if not ep.canManageProblem(u):
            raise Err(request, 'no priv')

        p = request.POST
        if request.method == 'POST':
            form = addProblemForm(request.POST)
        if not form.is_valid():
            raise Exception(u'数据输入有误')
        prb = ep
        data_count=prb.data_count
        case_info=prb.case_info

        if p['change_data'] == "1":
            dataInList=request.FILES.getlist('data_in')
            dataOutList=request.FILES.getlist('data_out')
            dataScrList=request.POST.getlist('data_scr')
            if len(dataInList)!=len(dataOutList) or len(dataInList)!=len(dataScrList):
                raise Exception(u'上传文件有误')
            for idx, nowData in enumerate(dataInList):
                path = Const.PROBLEM_DATA_PATH+str(prb.pid)+"/"+str(idx)+".in"
                if default_storage.exists(path):
                    default_storage.delete(path)
                default_storage.save(path, nowData)
            for idx, nowData in enumerate(dataOutList):
                path = Const.PROBLEM_DATA_PATH+str(prb.pid)+"/"+str(idx)+".out"
                if default_storage.exists(path):
                    default_storage.delete(path)
                default_storage.save(path, nowData)

            dict={}
            for idx, nowScr in enumerate(dataScrList):
                dict[str(idx)]=nowScr
            case_info=json.dumps(dict)

            data_count=len(dataInList)

        dict={}
        dict['desc']=p['prob_desc']
        dict['input_desc']=p['prob_input_desc']
        dict['output_desc']=p['prob_output_desc']
        dict['input_sample']=p['prob_input_sample']
        dict['output_sample']=p['prob_output_sample']
        prob_desc=json.dumps(dict)

        prb.updateProblem(prb.author.uid, p['prob_priv'], p['prob_title'], p['prob_time'],
                p['prob_memory'], p['prob_codelength'], prob_desc, p['is_spj'],
                data_count, p['course_id'], case_info)

        return redirect("/problem/p/"+str(prb.pid)+"/")
    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render(request, Err.ERROR_PAGE)

def getProblemTitle(request):
    logger.info(str(request).replace("\n","\t"))
    try:
        title = Problem.objects.get(pid=int(request.POST['pid'])).prob_title
    except:
        title = ""
    return HttpResponse(title)

def testUpload(request):
    logger.info(str(request).replace("\n","\t"))
    #if request.method == 'POST':
    #    return HttpResponse("POST")
    #if request.method == 'GETS':
    #    return HttpResponse("GETS")
    return HttpResponse("HEHE")
    #if default_storage.exists(path):
    #    default_storage.delete(path)
    #default_storage.save(path, nowData)

    #return HttpResponse()

def testUploadSubmit(request):
    logger.info(str(request).replace("\n","\t"))
    dataList = request.POST.getlist('scores')
    dict={}
    for idx, nowData in enumerate(dataList):
        dict[str(idx)]=nowData
    tjson=json.dumps(dict)
    td=json.loads(tjson)

    return HttpResponse(td["1"])


