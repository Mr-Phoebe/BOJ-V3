# coding: utf-8
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect, render_to_response

from django.core.urlresolvers import reverse

from Submission.models import Submission
from Problem.models import Problem
from User.models import User
from Contest.models import Contest, ContestProblem
from Course.models import *

from Submission.forms import addSubmissionForm, submissionListForm

from Submission.conf import JUDGE_RES_CN
from kari.const import Const
from common.err import Err

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.paginator import Paginator

from django.core.cache import cache
from datetime import datetime, timedelta
from Statistic.utils import *
import json

import logging

logger = logging.getLogger('django')

def index(request):
    logger.info(str(request).replace("\n\r","\t"))
    return HttpResponse("Here is status page!")

def submissionList(request, contest_id=None, page_id='1'):
    logger.info(str(request).replace("\n\r","\t"))
    """
    @view: list submission of some contest
    """

    try:
        page_id = int(page_id)
        u = User.getSessionUser(request.session)
        if not u:
            raise Err( request, err='not login')

        cid = int(contest_id)

        try:
            c = Contest.getById(cid)
        except:
            raise Err( request, err='no contest', 
                    log_format=( '{0}'.format(cid), ''), 
                    user_format=( u'{0}'.format( cid), u'别做坏事！'),
                    )

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

        isManager = c.course_class.canBeManaged(u)
        user = u if not isManager else None # privilege for showing all submissions

        idxList = [(cp.problem_index, cp.problem_index) for cp in c.getContestProblem()]
        langList = [('gcc','GNU C'), ('g++','GNU C++'), ('java','java')]
        form = submissionListForm(idxList, langList, request.GET)
        if form.is_valid():
            if form.cleaned_data['problem_index']:
                try:
                    contestProb = ContestProblem.getBy( c, form.cleaned_data['problem_index'])
                except:
                    contestProb=None
                    # raise Exception(u'contest problem not found')
            else:
                contestProb=None
        else:
            raise Err( request, err='example err', 
                    log_format=( 'form invalid', ''), 
                    user_format=( u'输入的内容不合法', '')
                    )

        #sub_all_c = getSUB()
        #submissions = bigfilter( u=user, c=c, cp=contestProb, uname=form.cleaned_data['username'], lang=form.cleaned_data['language'], sta=form.cleaned_data['status'])
        submissions = Submission.submissionList( u=user, c=c, cp=contestProb, uname=form.cleaned_data['username'], lang=form.cleaned_data['language'], sta=form.cleaned_data['status'])

        
        submissions = Submission.submissionList( u=user, c=c, cp=contestProb, uname=form.cleaned_data['username'], lang=form.cleaned_data['language'], sta=form.cleaned_data['status'])
        if isManager and 'rejudge' in request.GET and c.board_type != 2:
            map( lambda x: Submission.rejudgeSubmission( x), submissions)

        paginator = Paginator(submissions, Const.STATUS_PER_PAGE)
        page_id = min(max(int(page_id), 1), paginator.num_pages)

        s = paginator.page(page_id)

        for sub_s in s:
            sub_s.status_color = Const.STATUS_COLOR[sub_s.status] if sub_s.status in Const.STATUS_COLOR else ''
            sub_s.status_cn = Const.STATUS_CN[ sub_s.status]
        return render(request, 'newtpl/submission/status.html', {'sList':s, 'form':form, 'c':c, 'tpl':{'can_manage': True if isManager else False}})
        #return render(request, 'newtpl/submission/status.html', {'sList':s, 'form':form, 'c':c})

    except Exception as e:
        logger.error(str(e).replace("\n\r","\t"))
        return render(request, Err.ERROR_PAGE, { 'errmsg': unicode(e) } )

def addSubmission(request, contest_id=None, problem_index=None):
    logger.info(str(request).replace("\n\r","\t"))
    """
    view used to add submission
    """
    try:
        contest_id = int(contest_id)

        u = User.getSessionUser( request.session)
        if not u:
            raise Err( request, err='not login')

        if not contest_id:
            raise Err( request, err='request err', 
                    log_format=( 'contest id', 'UNDEFINED'), 
                    user_format=( u'考试编号', u'你吃了么！！！'),
                    )

        elif not problem_index:
            raise Err( request, err='request err', 
                    log_format=( 'problem index', 'UNDEFINED'), 
                    user_format=( u'题目序号', u'哪里去了！！'),
                    )
        else:
            try:
                c = Contest.getById( contest_id )
            except:
                raise Err( request, err='no contest', 
                        log_format=( '{0}'.format(cid), ''), 
                        user_format=( u'{0}'.format( cid), u'别做坏事！'),
                        )

            try:
                p_index = ContestProblem.getBy(c=c, idx=problem_index)
            except:
                raise Err( request, err='no contest problem', 
                        log_format=( '{0}'.format( problem_index), ''), 
                        user_format=( u'{0}'.format( problem_index), u'别乱写好么！！'),
                        )

            p = p_index.problem
            
            if not Submission.canSubmitCode( u, p_index ):
                raise Err( request, err = 'submit err', 
                        log_format = ( 'no priv to submit', 'contest ended or no priv to attend the contest'),
                        user_format = ( u'您没有提交该题的权限', u'考试已结束或者您没有参加本场考试的权限')
                        )

        lang_list = []
        if c.lang_limit & 1 == 1:
            lang_list.append( ('gcc','GNU C'))
        if (c.lang_limit >> 1) & 1 == 1:
            lang_list.append( ('g++','GNU C++'))
        if (c.lang_limit >> 2) & 1 == 1:
            lang_list.append( ('java', 'JAVA'))
            
        if request.method == 'POST':
            form = addSubmissionForm(lang_list, request.POST)

            if form.is_valid():
                sub_name = str( datetime.now())
                time_str = sub_name.split('.')
                time_str.pop()

                for i in ['-',':','.',' ']:
                    sub_name = sub_name.replace(i,'_')

                import os
                code_file_path = os.path.join( Const.SUBMISSION_TMP_PATH, "{0:010d}_{1}".format( u.uid, sub_name))
                code_length = 0

                # head_details: details of the submission added at the head of the code file
                head_details = ''
                head_details += '/*\n'
                head_details += 'USER_ID: ' + str(u) + '\n'
                head_details += 'PROBLEM: ' + str(p.pid) + '\n'
                head_details += 'SUBMISSION_TIME: ' + time_str[0] + '\n'
                head_details += '*/\n'

                if 'code_file' in request.FILES:
                    default_storage.save( code_file_path, request.FILES['code_file'])
                else:
                    if form.cleaned_data['code']:
                        default_storage.save( code_file_path, ContentFile( head_details + form.cleaned_data['code']))
                    else:
                        raise Err( request, err='request err', 
                                log_format=( 'code', 'no input'), 
                                user_format=( u'代码呢！', u'不写代码交什么交！！'),
                                )

                code_length = default_storage.size( code_file_path)
                sub_lang = form.cleaned_data['language']

                if sub_lang not in map( lambda x: x[0], lang_list):
                    raise Err( request, err='illegal language', 
                            log_format=( '{0}'.format( sub_lang), 'blabla'), 
                            user_format=( u'{0}'.format( sub_lang), u'别瞎搞成不！！'),
                            )

                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')

                additional = { 'submit_ip': ip}
                Submission.addSubmission( u, p_index, code_file_path, sub_lang, code_length, additional, c.board_type == 2)

                return redirect('Submission:contest_status',contest_id=contest_id) # could it be okay?
            else:
                raise Exception(u'form invalid')
            # the usage of url.name in urls.py
        # not POST method
        else:
            form = addSubmissionForm(lang_list)

        return render( request, 'newtpl/submission/submit.html', { 'form': form, 'tpl': {'sp':True}, 'contest': c, 'cp': p_index}, )# 'test_info': form.cleaned_data['language']})

    except Exception as e:
        logger.error(str(e).replace("\n\r","\t"))
        return render( request, Err.ERROR_PAGE, { 'errmsg': unicode(e), }, )

def OLDaddSubmission(request, contest_id=None, problem_index=None): # problem_id=None, 
    logger.info(str(request).replace("\n\r","\t"))
    """
    @view: add submission to some contest
    """
    template_tags = { 'show_cid': True, 'show_problem_index': True} # 'is_contest': False, 'show_pid': True, 
    u = None

    try:
        u = User.getSessionUser( request.session)
        if not u:
            return render( request, 'error.html', { 'errmsg': Const.NOT_LOGGED_IN}, )

        if request.method == 'POST':
            form = addSubmissionForm( request.POST)
            if form.is_valid():

                sub_name = str( datetime.now())
                for i in ['-',':','.',' ']:
                    sub_name = sub_name.replace(i,'_')
                code_file_path = "{0}/{1}_{2}".format(Const.SUBMISSION_TMP_PATH, u.uid, sub_name)
                code_length = 0
                if 'code_file' in request.FILES:
                        #return render( request, 'error.html', { 'errmsg': u'请选择要上传的文件！', 'user': u }, )
                    default_storage.save( code_file_path, request.FILES['code_file'])
                   # code_file = request.FILES['code_file']
                   # dest = open( code_file_path, 'wb+')
                   # for chunk in code_file.chunks():
                   #     code_length += len(chunk)
                   #     dest.write(chunk.encode('utf')) # chinese encoding
                        # dest.write(chunk)
                else:
                    if not form.cleaned_data['code']:
                        return render( request, 'error.html', { 'errmsg': u'请填写要提交的代码！', 'user': u }, )
                    default_storage.save( code_file_path, ContentFile( form.cleaned_data['code']))

                code_length = default_storage.size( code_file_path)
                    #dest = open( code_file_path, 'wb+')
                    #code_length = len(request.POST['code'])
                    #for chunk in request.POST['code']:
                    #    dest.write(chunk.encode('utf')) # chinese encoding
                    #dest.close()
                # before we tran the very file object, we should turn it off first!!!!(bugs here! but solved)

                no_judge = False
                if not contest_id:
                    return render( request, 'error.html', { 'errmsg': u'该选择要提交题目的考试！', 'user': u }, )
                else:
                    c = Contest.getById( contest_id )
                    if not c:
                        return render( request, 'error.html', { 'errmsg': u'编号为{0}的考试不存在！'.format( contest_id), 'user': u }, )

                    p_index = ContestProblem.getByContestAndProblemIndex( contest_id, form.cleaned_data['problem_index'])
                    if not p_index:
                        return render( request, 'error.html', { 'errmsg': u'序号为{0}的题目不存在于考试{1}中！'.format(form.cleaned_data['problem_index'], contest_id), 'user': u }, )
                    no_judge = c.board_type == 2
                    p = p_index.problem

                if not Submission.canSubmitCode( u, p.pid, contest_id):
                    return render( request, 'error.html', { 'errmsg': u'您没有提交本题的权限！', 'user': u}, )

                Submission.addSubmission( u, p_index, p.data_count, code_file_path, form.cleaned_data['language'], code_length, no_judge)

                return redirect('Submission:contest_status',contest_id=contest_id) # could it be okay?
            # the usage of url.name in urls.py
        # not POST method
        else:
            form = addSubmissionForm()
            if not contest_id:
                return render( request, 'error.html', { 'errmsg': u'该选择要提交题目的考试！', 'user': u }, )
            else:
                c = Contest.getById( contest_id )
                if not c:
                    return render( request, 'error.html', { 'errmsg': u'编号为{0}的考试不存在！'.format( contest_id), 'user': u }, )

        if problem_index:
            form.fields['problem_index'].initial = problem_index
        else:
            form.fields['problem_index'].initial = ''

        return render( request, 'Submission/Submit.html', { 'form': form, 'show_tags': template_tags, 'user': u, 'contest': c, 'problem_index': problem_index}, )# 'test_info': form.cleaned_data['language']})

    except Exception as e:
        logger.error(str(e).replace("\n\r","\t"))
        return render( request, 'error.html', { 'errmsg': unicode(e), 'user': u}, )

def rejudgeSubmission( request, sid):
    logger.info(str(request).replace("\n\r","\t"))
    """
    rejudge the very submission with the specific sid
    """
    try:
        sid = int( sid)
        u = User.getSessionUser( request.session)
        if not u:
            raise Err( request, err='not login')

        try:
            s = Submission.getById( sid)
        except:
            raise Err( request, err='no submission',
                    log_format=( '{0}'.format( sid), ''),
                    user_format=( u'{0}'.format( sid), u'不要搞笑！！'),
                    )

        if not s.problem_index.contest.course_class.canBeManaged( u):
            raise Err( request, err = 'no priv')

        Submission.rejudgeSubmission( s)

        return redirect( 'Submission:contest_status', contest_id=s.problem_index.contest.cid) 

    except Exception as e:
        logger.error(str(e).replace("\n\r","\t"))
        return render( request, Const.NEW_ERROR_PAGE, { 'errmsg': unicode(e), }, )

def viewCodeAndInfo( request, sid):
    logger.info(str(request).replace("\n\r","\t"))
    """
    view used to see details of the very submission
    """
    try:
        sid = int( sid)
        u = User.getSessionUser( request.session)
        if not u:
            raise Err( request, err='not login')

        try:
            s = Submission.getById( sid)
        except:
            raise Err( request, err='no submission',
                    log_format=( '{0}'.format( sid), ''),
                    user_format=( u'{0}'.format( sid), u'不要搞笑！！'),
                    )

        if not Submission.canViewCode( s, u):
            raise Err( request, err = 'no priv')

        info = eval( s.other_info)
        
        if 'ce' in info:
            info['ce'] = info['ce'].replace('/${TOKISAKI_KURUMI}', '')

        info['brush'] = Const.BRUSH[s.code_language]
        info['lang'] = Const.LANG_REFLECT[s.code_language]

        info['judger'] = Const.JUDGER_NAME
        info['user'] = s.user.uid
        info['judge_time'] = str(s.submission_time)
        info['status_cn'] = Const.STATUS_CN[info['status']]
        info['status_color'] = Const.STATUS_COLOR[info['status']] if info['status'] in Const.STATUS_COLOR else ''
        # info['submit_ip'] = request.META['REMOTE_ADDR']

        if 'score_sum' not in info:
            case_dict = json.loads(s.problem_index.problem.case_info)
            # score_sum = 0
            # for score in case_dict:
                # score_sum += int( score)
            score_sum = sum( map( int, case_dict.values()))
            info['score_sum'] = score_sum
            s.other_info = str( info)
            s.save()

        if 'case_result' in info:
            score_obtained = 0
            for seq in info['case_result']:
                seq['res_cn'] = JUDGE_RES_CN[seq['res']]
                temp_res = 'status-' + seq['res']
                seq['res_color'] = temp_res
                if 'score' in seq:
                    score_obtained += int(seq['score'])

            info['score_obtained'] = score_obtained

                # seq['res_color'] = Const.STATUS_COLOR[temp_res] if temp_res in Const.STATUS_COLOR else ''

        return render( request, 'newtpl/submission/code_and_info.html', { 'submission': s, 'info': info, 'code_content': default_storage.open(s.code_file).read().decode('utf-8','ignore'), 'tpl': { 'sp': True },  }, )

    except Exception as e:
        logger.error(str(e).replace("\n\r","\t"))
        return render( request, Err.ERROR_PAGE, { 'errmsg': unicode(e), }, )
