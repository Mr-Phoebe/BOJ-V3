# -*- coding: utf-8 -*-

from Contest.models import Contest, ContestProblem, ContestNotice, Clarification
from Contest.forms import contestForm, contestNoticeForm, ClarificationForm, AnswerClarificationForm
from User.models import User
from kari.const import Const
from Course.models import CourseClass
from Problem.models import Problem
from datetime import datetime, timedelta
from operator import add
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.contrib import messages
from common.utils import queryString
from common.err import Err
from Statistic.utils import getContestResult, getContestUserResult

import logging

logger = logging.getLogger('django')

def listContestByUser(request, pageId='1'):
    """
    view used to list all contest a user can participate
    """

    logger.info(str(request).replace("\n","\t"))
    tpl = {'nav_act':'contest'}

    try:
        u = User.getSessionUser(request.session)
        if not u:
            messages.info(request, u'请先登录')
            contestList = None
        else:
            now = datetime.now()
            if u.priv == 'student':
                contestList = Contest.getByStudent(u)
            else:
                contestList = Contest.getByAdmin(u)
                
            for c in contestList:
                c.course_class_name = unicode(c.course_class.getFullName())
                c.title = unicode(c.contest_title)
                if c.start_time+timedelta(minutes=c.length)<now:
                    c.status = 'ended'
                elif c.start_time > now:
                    c.status = 'scheduled'
                else:
                    c.status = 'running'

            paginator = Paginator(contestList, Const.CONTEST_PER_PAGE)
            pageId = min(max(int(pageId), 1), paginator.num_pages)

        if contestList and contestList.count>0:
            return render(request, 'newtpl/contest/contestListByUser.html', {
                'contest_list': paginator.page(pageId), 'tpl':tpl})
        else:
            return render(request, 'newtpl/contest/contestListByUser.html', {
                'tpl':tpl, 'err_msg_list': [
                    u'您暂时没有可以参加的测验。',
                    u'不如走出教室，呼吸一下新鲜空气，给家人打个电话，陪陪妹子？'
                    ]})

    except Exception as e:
        return render(request, Const.ERROR_PAGE, {'errmsg': unicode(e), })
    
def listContestByUserAll(request, pageId='1'):
    logger.info(str(request).replace("\n","\t"))
    tpl = {'nav_act':'contest'}

    try:
        u = User.getSessionUser(request.session)
        if not u:
            messages.info(request, u'请先登录')
            contestList = None
        else:
            now = datetime.now()
            if u.priv == 'student':
                contestList = Contest.getByUniversity(u.university)
            else:
                contestList = Contest.getByUniversity(u.university)
                
            for c in contestList:
                c.course_class_name = unicode(c.course_class.getFullName())
                c.title = unicode(c.contest_title)
                if c.start_time+timedelta(minutes=c.length)<now:
                    c.status = 'ended'
                elif c.start_time > now:
                    c.status = 'scheduled'
                else:
                    c.status = 'running'

            paginator = Paginator(contestList, Const.CONTEST_PER_PAGE)
            pageId = min(max(int(pageId), 1), paginator.num_pages)

        if contestList and contestList.count>0:
            return render(request, 'newtpl/contest/contestListByUserAll.html', {
                'contest_list': paginator.page(pageId), 'tpl':tpl})
        else:
            return render(request, 'newtpl/contest/contestListByUser.html', {
                'tpl':tpl, 'err_msg_list': [
                    u'您暂时没有可以参加的测验。',
                    u'不如走出教室，呼吸一下新鲜空气，给家人打个电话，陪陪妹子？'
                    ]})

    except Exception as e:
        return render(request, Const.ERROR_PAGE, {'errmsg': unicode(e), })
 
def listContestByUserAndPriv(request, pageId='1'):
    """
    view used to list all contest a user can manage
    """
    try:
        u = User.getSessionUser(request.session)
        if not u:
            messages.info(request, u'请先登录')
            return render(request, 'newtpl/contest/contestListByUserAndPriv.html')
            
        contestList = Contest.getByAdmin(u)
        now = datetime.now()
        
        for c in contestList:
            c.course_class_name = unicode(c.course_class.getFullName())
            c.title = unicode(c.contest_title)
            if c.start_time+timedelta(minutes=c.length)<now:
                c.status = 'ended'
            elif c.start_time > now:
                c.status = 'scheduled'
            else:
                c.status = 'running'

        paginator = Paginator(contestList, Const.CONTEST_PER_PAGE)
        pageId = min(max(int(pageId), 1), paginator.num_pages)
        return render(request, 'newtpl/contest/contestListByUserAndPriv.html', {
            'contest_list': paginator.page(pageId), 'tpl':{'has_priv': True, 'sp': True, }})
    except Exception as e:
        return render(request, Const.ERROR_PAGE, {'errmsg': unicode(e), })
    
def listContestByAuthor(request, pageId='1'):
    """
    view used to list all contest created by the specific user
    """
    try:
        u = User.getSessionUser(request.session)
        if not u:
            messages.info(request, u'请先登录')
            return render(request, 'newtpl/contest/contestListByAuthor.html')
            
        contestList = Contest.getByAuthor(u)
        now = datetime.now()
        for c in contestList:
            c.course_class_name = unicode(c.course_class.getFullName())
            c.title = unicode(c.contest_title)
            if c.start_time+timedelta(minutes=c.length)<now:
                c.status = 'ended'
            elif c.start_time > now:
                c.status = 'scheduled'
            else:
                c.status = 'running'

        paginator = Paginator(contestList, Const.CONTEST_PER_PAGE)
        pageId = min(max(int(pageId), 1), paginator.num_pages)
        return render(request, 'newtpl/contest/contestListByAuthor.html', {
            'contest_list': paginator.page(pageId), 'tpl':{'has_priv': True, 'nav_act':'contest',}})
    except Exception as e:
        return render(request, Const.ERROR_PAGE, {'errmsg': unicode(e), })
    
def listContest(request, ccId, pageId='1'):
    """
    view used to list all contest a user can participate, course_class restricted
    """
    try:
        u = User.getSessionUser(request.session)
        if not u:
            messages.info(request, u'请先登录')
            return render(request, 'newtpl/contest/contestList.html')
        
        cc = CourseClass.getById(ccId)
        Contest.canTouchContest(cc, u)
            
        now = datetime.now()
        contestList = Contest.getByCourseClass(cc)
            
        for c in contestList:
            c.course_class_name = unicode(c.course_class.getFullName())
            c.title = unicode(c.contest_title)
            if c.start_time+timedelta(minutes=c.length)<now:
                c.status = 'ended'
            elif c.start_time > now:
                c.status = 'scheduled'
            else:
                c.status = 'running'

        paginator = Paginator(contestList, Const.CONTEST_PER_PAGE)
        pageId = min(max(int(pageId), 1), paginator.num_pages)
        return render(request, 'newtpl/contest/contestList.html',
                      {'contest_list': paginator.page(pageId), 'course_class': cc, 'tpl':{'nav_act':'contest',}})
    except Exception as e:
        return render(request, Const.ERROR_PAGE, {'errmsg': unicode(e), })

def listContestByPriv(request, ccId, pageId='1'):
    """
    view used to list all contest a user can manage, course_class restricted
    """
    try:
        u = User.getSessionUser(request.session)
        if not u:
            messages.info(request, u'请先登录')
            return render(request, 'newtpl/contest/contestListByPriv.html')
        
        cc = CourseClass.getById(ccId)
        if not Contest.hasPriv(cc, u):
            raise Exception(Const.NOT_PVLG)
            
        contestList = Contest.getByCourseClass(cc)
        now = datetime.now()
        
        for c in contestList:
            c.course_class_name = unicode(c.course_class.getFullName())
            c.title = unicode(c.contest_title)
            if c.start_time+timedelta(minutes=c.length)<now:
                c.status = 'ended'
            elif c.start_time > now:
                c.status = 'scheduled'
            else:
                c.status = 'running'

        paginator = Paginator(contestList, Const.CONTEST_PER_PAGE)
        pageId = min(max(int(pageId), 1), paginator.num_pages)
        return render(request, 'newtpl/contest/contestListByPriv.html',
                      {'contest_list': paginator.page(pageId),  'course_class': cc,
                       'tpl':{'has_priv': True, 'nav_act':'contest',}})
    except Exception as e:
        return render(request, Const.ERROR_PAGE, {'errmsg': unicode(e), })

def _showContest(request, cId):
    cId = int(cId)

    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Exception(u'请先登录')

        c = Contest.getById(cId)
        c.canEnterContest(u)
        #cc = c.course_class

        c.course_class_name = unicode(c.course_class.getFullName())
        c.description = unicode(c.contest_description)
        c.title = unicode(c.contest_title)
        now = datetime.now()
        if c.start_time+timedelta(minutes=c.length) < now:
            c.status = 'ended'
        elif c.start_time > now:
            c.status = 'scheduled'
        else:
            c.status = 'running'
        c.time_passed = min(max(int((now-c.start_time).total_seconds())/60, 0), c.length)
        c.time_passed_percent = 100*c.time_passed/c.length
        c.time_left = c.length-c.time_passed

        cn = c.getContestNotice()

        if c.status != 'scheduled' or c.canUpdateContest(u):
            problemList = c.getContestProblem()
            for cp in problemList:
                cp.index = cp.problem_index
                cp.title = unicode(cp.problem_title)
                cp.tlim = cp.problem.prob_time
                cp.mlim = cp.problem.prob_memory

        return render(request, 'newtpl/contest/showContest.html',
                {'contest': c, 'problem_list': problemList, 'contest_notice_list': cn, 'ccid': c.course_class.id,
                    'tpl':{'has_priv': Contest.hasPriv(c.course_class, u),}})
    except Exception as e:
        return render(request, Const.ERROR_PAGE, {'errmsg':unicode(e),})

def showContest(request, cId):
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Err(request, 'not login')
        
        c = Contest.getById(cId)
        try:
            c.canEnterContest(u)
        except:
            raise Err(request, 'no priv')
        """
        cache_key = 'Contest' + str(cId)
        cache_result = cache.get(cache_key)
        if cache_result:
            return cache_result
        """


        cn = c.getContestNotice()
        c.course_class_name = unicode(c.course_class.getFullName())
        c.description = unicode(c.contest_description)
        c.title = unicode(c.contest_title)
        now = datetime.now()
        c.time_passed = min(max(int((now-c.start_time).total_seconds())/60, 0), c.length)
        c.time_passed_percent = 100*c.time_passed/c.length
        c.time_left = c.length-c.time_passed
        if c.start_time+timedelta(minutes=c.length)<now:
            c.status = 'ended'
        elif c.start_time > now:
            c.status = 'scheduled'
        else:
            c.status = 'running'
        priv = Contest.hasPriv(c.course_class, u)

        
        cache_key = 'Contestdict' + str(cId)
        res = cache.get(cache_key)
        if res:
            res['contest'] = c
            res['tpl']={'has_priv': priv, 'nav_act':'contest',}
            return render(request, 'newtpl/contest/showContest.html', res)
        
        problemList = c.getContestProblem()
        for cp, cp_res, cp_user_res in zip(problemList, getContestResult(c=c), getContestUserResult(c=c, u=u)):
            cp.index = cp.problem_index
            cp.title = unicode(cp.problem_title)
            cp.tlim = cp.problem.prob_time
            cp.mlim = cp.problem.prob_memory
            cp.ac = cp_res['ac_cnt']
            cp.sub = cp_res['sub_cnt']
            cp.ratio = cp_res['ac_ratio']
            #cp.user_res = cp_user_res


        res = {'contest': c, 'problem_list': problemList, 'contest_notice_list':cn,'ccid': c.course_class.id, 'tpl':{'has_priv': priv, 'nav_act':'contest',}}
        cache.set(cache_key, res, Const.CACHE_TIME_FIRST ) 
        return render(request, 'newtpl/contest/showContest.html', res)
        #res = render(request, 'newtpl/contest/showContest.html', {'contest': c, 'problem_list': problemList, 'contest_notice_list':cn,'ccid': c.course_class.id, 'tpl':{'has_priv': priv, 'nav_act':'contest',}})
        #cache.set(cache_key, res, 5 ) 
        #return res
    except Exception as e:
        return render(request, Err.ERROR_PAGE, {'errmsg': unicode(e), })

def chooseCourseClass(request):
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Err(request, 'not login')
        if u.isStudent():
            raise Err(request, 'no priv')
        cc_list = CourseClass.getAllManagedClasses(u)

        return render(request,'newtpl/contest/chooseCourseClass.html',{'list': cc_list, 'tpl':{'sp':True}})
    except Exception as e:
        return render(request, Err.ERROR_PAGE)

def addContest(request, ccId):
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Err(request, 'not login')
        
        try:
            cc = CourseClass.getById(ccId)
        except:
            raise Err(request, 'no resource')

        try:
            Contest.canAddContest(cc, u)
        except:
            raise Err(request, 'no priv')

        recentProblem = Problem.problemListByAuthor(u)

        if request.method == 'POST':
            form = contestForm(request.POST)
            pIdList = request.POST.getlist('problem_id')
            #pIdList =  Problem.problemList(u)

            pTitleList = request.POST.getlist('problem_title_custom')
            pCnt = len(pIdList)
            if form.is_valid():
                for i in xrange(pCnt):
                    p = Problem.getById(pIdList[i])
                    if not p.canViewProblem(u):
                        raise Err(request, 'no problem priv')

                pInfos = [(pIdList[i], pTitleList[i], chr(65+i)) for i in xrange(pCnt)]
                cTitle = form.cleaned_data['title']
                cDesc = form.cleaned_data['desc']
                cStartDate = form.cleaned_data['start_date']
                cStartTime = form.cleaned_data['start_time']
                cLength = form.cleaned_data['length']
                cBoardStop = form.cleaned_data['board_stop']
                cType = form.cleaned_data['contest_type']
                cBoardType = form.cleaned_data['board_type']
                permitLang = reduce(add, [Const.LANG_MASK[lang] for lang in form.cleaned_data['lang_limit']])
                c = Contest.addContest(u, cc, cTitle, pInfos, datetime.combine(cStartDate, cStartTime),
                                       cDesc, cLength, cBoardStop, cType, cBoardType, permitLang)
                return redirect('Contest:show_contest', c.cid)
            else:
                problemList = [{'pid': pIdList[x], 'title': pTitleList[x], 'origTitle':Problem.getById(pIdList[x]).prob_title} for x in xrange(pCnt)]
                return render(request, 'newtpl/contest/addContest.html', {'cc':cc,
                    'form': form, 'recent_problem': recentProblem,
                               'problem_list': problemList, 'tpl':{'has_priv': True, 'sp': True, }})
        else:
            form = contestForm()
            return render(request, 'newtpl/contest/addContest.html', {'cc':cc,
                'form': form, 'recent_problem': recentProblem, 
                'tpl':{'has_priv': True, 'sp': True, }})
    except Exception as e:
        messages.info(request, unicode(e))
        return render(request, Err.ERROR_PAGE)

def updateContest(request, cId):
    try:
        u = User.getSessionUser(request.session)
        if not u:
            #raise Exception(Const.NOT_LOGGED_IN)
            raise Err(request, err='not login')
        
        try:
            c = Contest.getById(cId)
        except:
            raise Err(request, 'no resource')
        cc = c.course_class

        try:
            c.canBeManaged(u)
        except:
            raise Err(request, err='no priv')

        started = c.isStarted(5)
        if started:
            recentProblem = None
        else:
            recentProblem = Problem.problemListByAuthor(u)

        problemList = [{'pid': cp.problem.pid, 'title': cp.problem_title, 'origTitle':cp.problem.prob_title} for cp in c.getContestProblem()]
        if request.method == 'POST':
            POST = request.POST.copy()
            if started:
                POST['start_date'] = c.start_time.date()
                POST['start_time'] = c.start_time.time()
                POST['started'] = started
            form = contestForm(POST)
            if started:
                form.fields['start_date'].widget.attrs['disabled'] = True
                form.fields['start_time'].widget.attrs['disabled'] = True
            if started:
                pIdList = [cp['pid'] for cp in problemList]
                pTitleList = [cp['title'] for cp in problemList]
                pass
            else:
                #pIdList =  Problem.problemList(u)
                pIdList = request.POST.getlist('problem_id')
                pTitleList = request.POST.getlist('problem_title_custom')
            pCnt = len(pIdList)
            if form.is_valid():
                for i in xrange(pCnt):
                    p = Problem.getById(pIdList[i])
                    if not p.canViewProblem(u):
                        raise Err(request, 'no problem priv')

                pInfos = [(pIdList[i], pTitleList[i], chr(65+i)) for i in xrange(pCnt)]
                cTitle = form.cleaned_data['title']
                cDesc = form.cleaned_data['desc']
                cStartDate = form.cleaned_data['start_date']
                cStartTime = form.cleaned_data['start_time']
                cLength = form.cleaned_data['length']
                cBoardStop = form.cleaned_data['board_stop']
                cType = form.cleaned_data['contest_type']
                cBoardType = form.cleaned_data['board_type']
                permitLang = reduce(add, [Const.LANG_MASK[lang] for lang in form.cleaned_data['lang_limit']])
                c.updateContest(cTitle, pInfos, datetime.combine(cStartDate, cStartTime), cDesc,
                                cLength, cBoardStop, cType, cBoardType, permitLang)
                return redirect('Contest:show_contest', cId)
            else:
                problemList = [{'pid': pIdList[x], 'title': pTitleList[x], 'origTitle':Problem.getById(pIdList[x]).prob_title} for x in xrange(pCnt)]
                return render(request, 'newtpl/contest/updateContest.html',
                        {'c': c, 'cc':cc, 'form': form, 'started': started, 'hehe':pCnt, 'recent_problem':recentProblem,
                               'problem_list': problemList, 'tpl':{'has_priv': True, 'sp': True,}})
        else:
            form = contestForm(
                    initial={
                        'title': c.contest_title,
                        'desc':c.contest_description, 
                        'start_date': c.start_time.date(),
                        'start_time': c.start_time.time(),
                        'length': c.length,
                        'board_stop': c.board_stop,
                        'contest_type': c.contest_type,
                        'board_type': c.board_type,
                        'lang_limit': c.permittedLangs(),
                        'started': started,
                        }
                    )
            if started:
                form.fields['start_date'].widget.attrs['disabled'] = True
                form.fields['start_time'].widget.attrs['disabled'] = True
            return render(request, 'newtpl/contest/updateContest.html',
                    {'c':c, 'cc':cc, 'form': form, 'started': started, 'recent_problem':recentProblem,
                           'problem_list': problemList, 'tpl':{'has_priv': True, 'sp': True, 'nav_act':'contest',}})
            #return render(request, Const.ERROR_PAGE, {'errmsg': unicode(e), })
    except Exception as e:
        messages.info(request, unicode(e))
        return render(request, Const.ERROR_PAGE, {'errmsg': unicode(e), })

def releaseBoardTime(request, cId):
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Exception(Const.NOT_LOGGED_IN)
        try:
            c = Contest.getById(cId)
        except:
            raise Err(request, 'no resource')
        try:
            c.canBeManaged(u)
        except:
            raise Err(request, err='no priv')

        c = Contest.getById(cId)
        c.board_stop = c.length
        c.save()
        return redirect('Contest:show_contest', cId)
    except Exception as e:
        return render(request, Const.ERROR_PAGE, {'errmsg': unicode(e), })

def listContestNotice(request, cId):
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Exception(Const.NOT_LOGGED_IN)
            
        c = Contest.getById(cId)
        c.canEnterContest(u)
        cn = c.getContestNotice()
        return render(request, 'newtpl/contest/contestNoticeList.html',
                { 'cid': cId, 'contest_notice_list':c.getContestNotice(),
                'tpl':{'has_priv': Contest.hasPriv(c.course_class, u), 'nav_act':'contest',}})
    except Exception as e:
        return render(request, Const.ERROR_PAGE, {'errmsg': unicode(e), })

def showContestNotice(request, cId, cnId):
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Exception(Const.NOT_LOGGED_IN)
        
        c = Contest.getById(cId)
        cn = ContestNotice.getById(cnId)
        c.canEnterContest(u)
        return render(request, 'newtpl/contest/showContestNotice.html',
                      {'cid': cId, 'contest_notice': cn,
                       'tpl': {'has_priv': Contest.hasPriv(c.course_class, u), 'sp': True, 'nav_act':'contest',}})
    except Exception as e:
        return render(request, Const.ERROR_PAGE, {'errmsg': unicode(e), })

def addContestNotice(request, cId):
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Exception(Const.NOT_LOGGED_IN)
        
        c = Contest.getById(cId)
        c.canBeManaged(u)
        
        if request.method == 'POST':
            form = contestNoticeForm(request.POST)
            if form.is_valid():
                cnTitle = form.cleaned_data['title']
                cnContent = form.cleaned_data['content']
                cn = c.addNotice(cnTitle, cnContent)
                return redirect('Contest:show_contest_notice', cId, cn.id)
            else:
                return render(request, 'newtpl/contest/addContestNotice.html',
                          {'form': form, 'cid': cId, 'tpl':{'has_priv': True, 'sp': True, 'nav_act':'contest',}})
        else:
            form = contestNoticeForm()
            return render(request, 'newtpl/contest/addContestNotice.html',
                          {'form': form, 'cid': cId, 'tpl':{'has_priv': True, 'sp': True, 'nav_act':'contest',}})
    except Exception as e:
        return render(request, Const.ERROR_PAGE, {'errmsg': unicode(e), })

def updateContestNotice(request, cId, cnId):
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Exception(Const.NOT_LOGGED_IN)
        
        c = Contest.getById(cId)
        cn = ContestNotice.getById(cnId)
        c.canBeManaged(u)
        
        if request.method == 'POST':
            form = contestNoticeForm(request.POST)
            if form.is_valid():
                cnTitle = form.cleaned_data['title']
                cnContent = form.cleaned_data['content']
                cn.updateNotice(cnTitle, cnContent)
                return redirect('Contest:show_contest_notice', cId, cn.id)
            else:
                return render(request, 'newtpl/contest/updateContestNotice.html',
                              {'form': form, 'cid': cId, 'cnid': cnId,
                           'tpl':{'has_priv': True, 'sp': True, 'nav_act':'contest',}})
        else:
            form = contestNoticeForm(
                initial={
                    'title': cn.notice_title,
                    'content': cn.notice_content,
                    }
            )
            return render(request, 'newtpl/contest/updateContestNotice.html',
                          {'form': form, 'cid': cId, 'cnid': cnId,
                           'tpl':{'has_priv': True, 'sp': True, 'nav_act':'contest',}})
    except Exception as e:
        return render(request, Const.ERROR_PAGE, {'errmsg': unicode(e), })

def getContestNoticeList(request):
    cId = request.POST['cid']
    c = Contest.getById(cId)
    f = lambda cn: '<a href="' + reverse('Contest:show_contest_notice', args=[cId, cn.id]) + '">' + cn.notice_title + '</a>'
    return HttpResponse(' '.join([f(cn) for cn in c.getContestNotice()]))

def viewAllClarifications(request, cid):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Exception(Const.NOT_LOGGED_IN) 
        
        cache_c = 'Clar_c' + str(cid)
        c = cache.get(cache_c)
        if not c:
            c = Contest.getById(cid)
            cache.set(cache_c, c, Const.CACHE_TIME_CLAFI)
        
        
        cache_cs = 'Clar_cs' + str(cid)
        cs = cache.get(cache_cs)
        if not cs:
            cs = Clarification.getByContestId(cid)
            cache.set(cache_cs, cs, Const.CACHE_TIME_CLAFI)
        if not c:
            raise Exception(Const.CONTEST_NOT_EXIST)

        try:
            c.canEnterContest(u)
            can_add_clar = True
        except:
            can_add_clar = False

        try:
            c.canBeManaged(u)
            can_update_clar = True
        except:
            can_update_clar = False
        return render(request, 'newtpl/contest/viewAllClars.html', {'clars': cs, 'contest': c, 'can_add_clar': can_add_clar, 'can_update_clar': can_update_clar})

    except Exception as e:
        logger.error(unicode(e).replace('\n', '\t')) 
        return render(request, Err.ERROR_PAGE, {'errmsg': unicode(e)})    

def addClarification(request, cid):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Exception(Const.NOT_LOGGED_IN)
        c = Contest.getById(cid)
        if not c:
            raise Exception(Const.CONTEST_NOT_EXIST)

        has_priv = False
        try:
            c.canBeManaged(u)
            has_priv = True
        except:
            pass
        try:
            c.canEnterContest(u)
            has_priv = True
        except:
            pass
        if not has_priv:
            raise Exception('No Privilege!')
        
        if request.method != 'POST':
            return render(request, 'newtpl/contest/addClar.html', {'contest': c})

        form = ClarificationForm(request.POST)
        try:
            if form.is_valid():
                question = form.cleaned_data['question']
                Clarification.addClarification(question, u, c)
                return redirect('Contest:view_all_clars', cid)
            else:
                raise
        except:
            raise Exception('Invalid Question')
    except Exception as e:
        logger.error(unicode(e).replace('\n', '\t')) 
        return render(request, Err.ERROR_PAGE, {'errmsg': unicode(e)})    

def answerClarification(request, clar_id):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Exception(Const.NOT_LOGGED_IN)
        clar = Clarification.getById(clar_id)
        if not clar:
            raise Exception('No such Clarification!')
        c = clar.contest
        if not c:
            raise Exception(Const.CONTEST_NOT_EXIST)
        try:
            c.canBeManaged(u)
        except:
            raise Exception('No Privilege!')
        
        if request.method != 'POST':
            return render(request, 'newtpl/contest/answerClar.html', {'clar': clar})

        form = AnswerClarificationForm(request.POST)
        try:
            if form.is_valid():
                answer = form.cleaned_data['answer']
                clar.updateAnswer(answer, u)
                return redirect('Contest:view_all_clars', c.cid)
            else:
                raise Exception('Invalid Answer!')
        except Exception as e:
            raise e
    except Exception as e:
        logger.error(unicode(e).replace('\n', '\t')) 
        return render(request, Err.ERROR_PAGE, {'errmsg': unicode(e)})    

def deleteClarification(request, clar_id):
    logger.info(str(request).replace("\n","\t"))
    try:
        u = User.getSessionUser(request.session)
        if not u:
            raise Exception(Const.NOT_LOGGED_IN)
        clar = Clarification.getById(clar_id)
        if not clar:
            raise Exception('No such Clarification!')
        c = clar.contest
        if not c:
            raise Exception(Const.CONTEST_NOT_EXIST)
        try:
            c.canBeManaged(u)
        except:
            raise Exception('No Privilege!')
        
        clar.deleteClarification()
        return redirect('Contest:view_all_clars', c.pk)
    except Exception as e:
        logger.error(unicode(e).replace('\n', '\t')) 
        return render(request, Err.ERROR_PAGE, {'errmsg': unicode(e)})    

