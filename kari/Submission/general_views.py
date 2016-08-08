# coding: utf-8
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect, render_to_response

from django.core.urlresolvers import reverse

from Submission.models import GeneralSubmission
from Problem.models import Problem
from User.models import User

from Submission.general_forms import addGeneralForm, generalListForm

from Submission.conf import JUDGE_RES_CN
from kari.const import Const
from common.err import Err

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.paginator import Paginator

from datetime import datetime, timedelta

import json

def index(request):
    return HttpResponse("Here is general status page!")

def generalSubmissionList(request, page_id='1'):
    """
    @view: list general submission
    """

    try:
        page_id = int(page_id)
        u = User.getSessionUser(request.session)
        if not u:
            raise Err( request, err='not login')
        
        # fake
        if u.priv == 'university':
            has_priv = True
        else:
            has_priv = False

        user = u if not has_priv else None
        
        lang_list = [('gcc','GNU C'), ('g++','GNU C++'), ('java','java')]
        form = generalListForm( lang_list, request.GET)
        if form.is_valid():
            if form.cleaned_data['problem_id']:
                try:
                    p = Problem.getById( form.cleaned_data['problem_id'])
                except:
                    raise Err( request, err='request err', 
                            log_format=( 'form invalid', 'problem_id error'), 
                            user_format=( u'输入的内容不合法', u'没有这道题！')
                            )
            else:
                p = None
        else:
            raise Err( request, err='example err', 
                    log_format=( 'form invalid', ''), 
                    user_format=( u'输入的内容不合法', '')
                    )

        g_subs = GeneralSubmission.generalSubmissionList( u=user, p=p, uname=form.cleaned_data['username'], language=form.cleaned_data['language'], status_selected=form.cleaned_data['status'], university=u.university)

        if 'rejudge' in request.GET:
            if has_priv:
                map( lambda x: GeneralSubmission.rejudgeGeneralSubmission( x), g_subs)
            else:
                raise Err( request, err = 'no priv')

        paginator = Paginator( g_subs, Const.STATUS_PER_PAGE)
        page_id = min(max(int(page_id), 1), paginator.num_pages)

        g_s = paginator.page(page_id)

        for g_s_index in g_s:
            g_s_index.status_color = Const.STATUS_COLOR[g_s_index.status] if g_s_index.status in Const.STATUS_COLOR else ''
            g_s_index.status_cn = Const.STATUS_CN[ g_s_index.status]
        return render(request, 'newtpl/submission/general/status.html', {'general_list': g_s, 'form':form, 'tpl':{'can_manage': True if has_priv else False}})

    except Exception as e:
        return render(request, Err.ERROR_PAGE, { 'errmsg': unicode(e) } )

        # here
def addGeneralSubmission(request, problem_id=None): 
    """
    view used to add general submission
    """
    try:
        if not problem_id:
            raise Err( request, err='request err', 
                    log_format=( 'problem index', 'UNDEFINED'), 
                    user_format=( u'题目序号', u'哪里去了！！'),
                    )
            
        problem_id = int( problem_id)

        try:
            p = Problem.getById( problem_id)
        except:
            raise Err( request, err='no problem', 
                    log_format=( '{0}'.format( problem_id), ''), 
                    user_format=( u'{0}'.format( problem_id), u'啥乱七八糟的！！！'),
                    )

        u = User.getSessionUser( request.session)
        if not u:
            raise Err( request, err='not login')


            if not GeneralSubmission.canSubmitCode( u, p):
                raise Err( request, err = 'no priv')

        if request.method == 'POST':
            lang_list = [('gcc','GNU C'), ('g++','GNU C++'), ('java', 'JAVA')]

            form = addGeneralForm(lang_list, request.POST)

            if form.is_valid():

                sub_name = str( datetime.now())
                time_str = sub_name.split('.')
                time_str.pop()

                for i in ['-',':','.',' ']:
                    sub_name = sub_name.replace(i,'_')

                head_details = ''
                head_details += '/*\n'
                head_details += 'USER_ID: ' + str(u) + '\n'
                head_details += 'PROBLEM: ' + str(p.pid) + '\n'
                head_details += 'SUBMISSION_TIME: ' + time_str[0] + '\n'
                head_details += '*/\n'

                import os
                code_file_path = os.path.join( Const.SUBMISSION_TMP_PATH, "{0:010d}_{1}_{2}".format( u.uid, sub_name, 'general'))
                code_length = 0

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

                GeneralSubmission.addGeneralSubmission( u, p, code_file_path, form.cleaned_data['language'], code_length)

                return redirect('Submission:status') # could it be okay?

            else:
                raise Exception(u'form invalid')

        # not POST method
        else:
            lang_list = [('gcc','GNU C'), ('g++','GNU C++'), ('java', 'JAVA')]
            form = addGeneralForm(lang_list)

        return render( request, 'newtpl/submission/general/submit.html', { 'form': form, 'tpl': {'sp': True}, 'problem':p }, )

    except Exception as e:
        return render( request, Err.ERROR_PAGE, { 'errmsg': unicode(e), }, )

def rejudgeGeneralSubmission( request, gsid):
    """
    rejudge the very general submission with the specific id
    """
    try:
        gsid = int( gsid)
        u = User.getSessionUser( request.session)
        if not u:
            raise Err( request, err='not login')

        try:
            g_s = GeneralSubmission.getById( gsid)
        except:
            raise Err( request, err='no generalsubmission',
                    log_format=( '{0}'.format( gsid), ''),
                    user_format=( u'{0}'.format( gsid), u'别扯了！！'),
                    )

        # fake
        if u.priv == 'student':
            raise Err( request, err = 'no priv')

        GeneralSubmission.rejudgeGeneralSubmission( g_s)

        return redirect( 'Submission:status')

    except Exception as e:
        return render( request, Const.NEW_ERROR_PAGE, { 'errmsg': unicode(e), }, )

def viewCodeAndInfo( request, gsid):
    """
    view used to show the detail of some general submission
    """
    try:
        gsid = int( gsid)
        u = User.getSessionUser( request.session)
        if not u:
            raise Err( request, err = 'not login')

        try:
            g_s = GeneralSubmission.getById( gsid)
        except:
            raise Err( request, err='no generalsubmission',
                    log_format=( '{0}'.format( gsid), ''),
                    user_format=( u'{0}'.format( gsid), u'别扯了！！'),
                    )

        if not GeneralSubmission.canViewCode( g_s, u):
            raise Err( request, err = 'no priv')

        info = eval( g_s.other_info)
        info['brush'] = Const.BRUSH[g_s.code_language]
        info['status_cn'] = Const.STATUS_CN[info['status']]
        info['status_color'] = Const.STATUS_COLOR[info['status']] if info['status'] in Const.STATUS_COLOR else ''
        info['lang'] = Const.LANG_REFLECT[g_s.code_language]
        info['judge_time'] = str(g_s.submission_time)
        info['judger'] = Const.JUDGER_NAME

        if 'ce' in info:
            info['ce'] = info['ce'].replace('/${TOKISAKI_KURUMI}', '')

        info['score_obtained'] = 0

        if 'score_sum' not in info:
            case_dict = json.loads(g_s.problem.case_info)
            score_sum = sum( map( int, case_dict.values()))
            info['score_sum'] = score_sum
            #g_s.other_info = str( info)
            #g_s.save()

        if 'case_result' in info:
            score_obtained = 0
            for seq in info['case_result']:
                seq['res_cn'] = JUDGE_RES_CN[seq['res']]
                temp_res = 'status-' + seq['res']
                seq['res_color'] = temp_res
                if 'score' in seq:
                    score_obtained += int(seq['score'])
            info['score_obtained'] = score_obtained


        # info['submit_ip'] = request.META['REMOTE_ADDR']

        # if 'score_sum' not in info:
        #     case_dict = json.loads(s.problem.case_info)
        #     # score_sum = 0
        #     # for score in case_dict:
        #         # score_sum += int( score)
        #     score_sum = sum( map( int, case_dict.values()))
        #     info['score_sum'] = score_sum
        #     s.other_info = str( info)
        #     s.save()

        #if 'case_result' in info:
        #    for seq in info['case_result']:
        #        seq['res_cn'] = JUDGE_RES_CN[seq['res']]

        return render( request, 'newtpl/submission/general/code_and_info.html', { 'submission': g_s, 'info': info, 'code_content': default_storage.open(g_s.code_file).read(), 'tpl': { 'sp': True } }, )

    except Exception as e:
        return render( request, Err.ERROR_PAGE, { 'errmsg': unicode(e),}, )
