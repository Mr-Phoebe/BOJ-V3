# coding: utf
from django.db import models
from django.core.paginator import Paginator

from kari.const import Const
from kari.conf import flush_transaction
from Submission.conf import *

import Core.tasks
from Problem.models import Problem
from Contest.models import Contest, ContestProblem
from Course.models import *

from User.models import User

import time
from datetime import datetime

from django.core.cache import cache
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import json

# Create your models here.

class Submission( models.Model):
    """
    Submission Information
    """

    # const str for Exception Message
    SUBMISSION_ID_NOT_EXIST = 'No such Submission with ID {0}'

    # primary key assigned as SID
    sid =models.AutoField( primary_key=True)

    # foreign keys
    user = models.ForeignKey('User.User', verbose_name='user of the submission', db_index=True)
    problem_index = models.ForeignKey('Contest.ContestProblem', verbose_name='problem index in the corresponding contest', db_index=True)

    # intrinsic values
    status =  models.CharField(max_length=20, choices=STATUS_ABBR, verbose_name='the returned status of the current submission', db_index=True)
    data_cnt = models.IntegerField( verbose_name='the number of data files of the very problem in the very submission')
    code_file = models.FilePathField( path='code', verbose_name='the file path of code files of the very submission')
    code_length = models.IntegerField( verbose_name='the length of the code described above')
    code_language = models.CharField( max_length=20, choices=Const.LANG, verbose_name='the programming language of the code of current submission')
    submission_time = models.DateTimeField( auto_now_add=True,verbose_name='the precise time of the very submission') # with the former option, it can be stamped at creation time
    run_time = models.IntegerField( verbose_name='the run time of the compiled code, in unit of ms')
    run_memory = models.IntegerField( verbose_name='the maximum memory allocated in run-time of the compliled code, in the unit of kb')
    other_info = models.TextField( default='', verbose_name='the additional info about the very submission, maybe in the type of json or xml or python dict')

    # atom function
    def __unicode__( self):
        return str(self.sid)

    # in parts below, we assume that all validations have been done 
    # in view layer

    @classmethod
    def getById( cls, sid):
        """
        get Submission by SID and validate SID
        """
        try:
            s = cls.objects.get(pk=sid)
        except:
            raise Exception( cls.SUBMISSION_ID_NOT_EXIST.format(sid))
        return s

    @classmethod
    def addSubmission( cls, user = None, problem_index = None, code_file_path = '', code_language = '', code_length = 0, ad_info = {}, no_judge = False):
        """
        add Submission, with user, problem_index( combined with contest and problem_id), data_count, code_file_path, code_language, code_length, no_judge
        ( now general submission is handled in another model)
        """
        # use instances as params to omit the validation, cause validation has been done in vies
        # we should add validator in views module

        try:
            s = Submission()
            other_info = ad_info.copy()

            s.user = user # user.submission_set.add may also be okay
            other_info['username'] = s.user.username

            s.problem_index = problem_index
            other_info['pid'] = s.problem_index.problem_id
            other_info['cid'] = s.problem_index.contest_id

            s.status = 'Pending'
            other_info['status'] = s.status

            s.data_cnt = s.problem_index.problem.data_count
            other_info['data_cnt'] = str(s.data_cnt)

            s.code_language = code_language
            other_info['code_language'] = code_language

            s.code_length = code_length
            other_info['code_length'] = str(code_length)

            s.run_time = 0
            other_info['run_time'] = str(s.run_time)
            s.run_memory = 0
            other_info['run_memory'] = str(s.run_memory)

            # for scoring
            other_info['score'] = str(0)

            s.other_info = str(other_info)

            s.submission_time = datetime.now()

            s.save()
            flush_transaction()

            import os
            true_addr = os.path.join( Const.SUBMISSION_CODE_PATH, str(s.sid))
            if default_storage.exists( true_addr): # bugs came out as versions updated
                default_storage.delete( true_addr)

            default_storage.save( true_addr, default_storage.open(code_file_path))
            # the second param is a FILE object or its subclass
            default_storage.delete( code_file_path)
            s.code_file = true_addr

            other_info = eval(s.other_info)
            other_info['code_file_path'] = s.code_file

            # cause we don't have it at former time
            other_info['submit_time'] = str(s.submission_time)

            s.other_info = str(other_info)

            s.save()
            flush_transaction()

            sent_to_queue = False
            if no_judge == True:
                # Never judge
                s.status = 'Accepted'
                s.save()
                sent_to_queue = True
            while not sent_to_queue:
                try:
                    Core.tasks.JudgeQueue.sendJudge(_sid= s.sid, _pid= s.problem_index.problem_id, _lang= s.code_language,
                            _mode='contest', _code_path=s.code_file)
                    sent_to_queue = True
                except Exception as e:
                    print str(e)

            return s.sid

        except:
            raise

    @classmethod
    def rejudgeSubmission(cls, s, no_judge = False):
        """
        func used to rejudge the very submission
        """

        # no need to handle exception?
        # or exception transmission?
        try:
            if no_judge == True:
                s.status = 'Accepted'
                s.save()
                return True
            info = eval(s.other_info)
            s.status = 'Rejudging'
            info['status'] = s.status
            s.run_time = 0
            info['run_time'] = str(s.run_time)
            s.run_memory = 0
            info['run_memory'] = str(s.run_memory)
            s.other_info = str(info)

            # for scoring
            info['score'] = str(0)

            s.save()
            flush_transaction()

            sent_to_queue = False
            while not sent_to_queue:
                try:
                    Core.tasks.JudgeQueue.sendJudge(_sid= s.sid, _pid= s.problem_index.problem_id, _lang= s.code_language,
                            _mode='contest', _code_path=s.code_file)
                    sent_to_queue = True
                except Exception as e:
                    print str(e)

            return True

        except:
            raise

    @classmethod
    def updateSubmission( cls, sid, judge_info):
        """
        called by JudgeQueue
        save dict in other_info as str
        """

        try:
            s = cls.getById( sid)

            print judge_info
            s.status = SUB_STATUS[judge_info['status']]
            info = eval( s.other_info)

            if s.status == 'Init':
                s.status = 'System Error'
                s.run_time = 0
                s.run_memory = 0
                info['run_time'] = str(s.run_time)
                info['run_memory'] = str(s.run_memory)
                info['case_judged'] = str(0)
                info['score'] = str(0)

            elif s.status == 'Compile Error':
                s.run_time = 0
                s.run_memory = 0
                info['run_time'] = str(s.run_time)
                info['run_memory'] = str(s.run_memory)
                info['ce'] = judge_info['ce']
                info['case_judged'] = str(0)
                info['score'] = str(0)

            elif s.status != 'Compiling' and s.status != 'Judging':
                s.run_time = judge_info['time']
                s.run_memory = judge_info['mem']
                info['run_time'] = str(s.run_time)
                info['run_memory'] = str(s.run_memory)

                s.status = 'Judging'
                seq = []
                jd_cnt = 0
                case_dict = json.loads(s.problem_index.problem.case_info)
                temp_score = 0
                for seq_res in judge_info['case_res']:
                    if jd_cnt >= judge_info['case_done']:
                        break

                    if s.status == 'Judging':
                        if seq_res['res'] == 'se':
                            s.status = JUDGE_RES['se']
                        elif seq_res['res'] == 're':
                            s.status = JUDGE_RES['re']
                        elif seq_res['res'] == 'mle':
                            s.status = JUDGE_RES['mle']
                        elif seq_res['res'] == 'tle':
                            s.status = JUDGE_RES['tle']
                        elif seq_res['res'] == 'wa':
                            s.status = JUDGE_RES['wa']
                        elif seq_res['res'] == 'pe':
                            s.status = JUDGE_RES['pe']
                        elif seq_res['res'] == 'ole':
                            s.status = JUDGE_RES['ole']

                    if seq_res['res'] == 'ac':
                        if not case_dict[str(jd_cnt)].isdigit():
                            raise Exception( "Invalid Score")
                        temp_score += int(case_dict[str(jd_cnt)])
                        seq_res['score'] = case_dict[str(jd_cnt)]

                    seq.append(seq_res)
                    jd_cnt += 1

                info['case_judged'] = judge_info['case_done']
                info['case_result'] = seq
                info['score'] = str(temp_score)

                if s.status == 'Judging':
                    s.status = 'Accepted'

            info['status'] = s.status

            s.other_info = str( info)
            s.save() # without such sentence, no data modification will be updated
            flush_transaction()

            return True

        except:
            raise

    @classmethod
    def submissionList(cls, u=None, c=None, cp=None, uname=None, lang=None, sta=None, board_stop_time=None):
        """
        return the submission list filter by params
        """

        try:
            s = cls.objects.prefetch_related('user', 'problem_index')
            if u:
                s = s.filter(user=u)
            elif uname:
                s = s.filter(user__username__icontains=uname)
            if cp:
                s = s.filter(problem_index=cp)
            elif c:
                s = s.filter(problem_index__contest=c)
            else:
                raise Exception('evil query')
            if sta:
                s = s.filter(status=sta)
            if lang:
                s = s.filter(code_language=lang)
            if board_stop_time:
                s = s.filter(submission_time__lt=board_stop_time)
            s = s.order_by('-sid')
            #s_num = s.count()
            return s
        
        except:
            raise

    @classmethod
    def submissionListOld( cls, uid=None, pid=None, cid=None, uname=None, language=None, status_selected=None):
        """
        return the submission list filter by params
        """
        # use 'not' to judge None and ''
        # then no 'not' as True

        # and we should get pid by cid and p_index, so we have no need to use them here
        submissions = cls.objects.all()
        if pid:
            submissions = submissions.filter(problem_index__problem_id=pid) # bugs fixed here, we should use __ instead of . to avoid using expression
        if cid:
            submissions = submissions.filter(problem_index__contest_id=cid)
        if uid:
            submissions = submissions.filter(user_id=uid)
        if uname:
            submissions = submissions.filter(user__username__icontains=uname) # omit CASE and search implicitly
        if language:
            submissions = submissions.filter(code_language=language)
        if status_selected:
            submissions = submissions.filter(status=status_selected)
        submissions = submissions.order_by('-sid')
        num_submissions = submissions.count()
        # bugs here, logic uncorrect
        # pages = num_submissions / Const.STATUS_PER_PAGE + ( ( num_submissions % Const.STATUS_PER_PAGE) > 0)
        # page_id = min( max( 1, page_id), pages if pages > 0 else pages+1)
        # id_begin = ( page_id - 1) * Const.STATUS_PER_PAGE
        # id_end = min( page_id * Const.STATUS_PER_PAGE, num_submissions)
        return submissions #[id_begin:id_end]

    @classmethod
    def canViewCode( cls, s, user):
        """
        if user could view code of the submission or not
        """

        try:
            #when a important contest is running
            #if user.priv == 'student':
            #    return False
            if s.user == user:
                return True
            else:
                # university, school, course, course_class admin can view
                if not s.problem_index.contest.course_class.canBeManaged( user):
                   return False
                return True 

        except:
            raise

    @classmethod
    def canSubmitCode( cls, user, problem_index ):
        """
        if user could submit some code to the specific problem in a specific contestor not
        """

        try:
            return (not problem_index.contest.isEnded()) and problem_index.contest.canEnterContest( user)

        except:
            raise

class GeneralSubmission( models.Model):
    """
    General Submission Information
    """
    # const str for Exception Message
    GENERAL_SUBMISSION_ID_NOT_EXIST = 'No such General Submission wit ID {0}'

    # foreign keys
    user = models.ForeignKey( 'User.User', verbose_name='user of the submission')
    problem = models.ForeignKey( 'Problem.Problem', verbose_name='problem id')

    # intrinsic values
    status =  models.CharField( max_length=20, choices=STATUS_ABBR, db_index=True, verbose_name='the returned status of the current submission')
    data_cnt = models.IntegerField( verbose_name='the number of data files of the very problem in the very submission')
    code_file = models.FilePathField( path='code', verbose_name='the file path of code files of the very submission')
    code_length = models.IntegerField( verbose_name='the lenght of the code described above')
    code_language = models.CharField( max_length=20, choices=Const.LANG, verbose_name='the programming language of the code of current submission')
    submission_time = models.DateTimeField( auto_now_add=True,verbose_name='the precise time of the very submission') # with the former option, it can be stamped at creation time
    run_time = models.IntegerField( verbose_name='the run time of the compliled code, in the unit of ms')
    run_memory = models.IntegerField( verbose_name='the maximum memory allocated in run-time of the compliled code, in the unit of kb')
    other_info = models.TextField( default='', verbose_name='the additional info about the very submission, maybe in the type of json or xml or python dict')

    # atom function
    def __unicode__( self):
        return str(self.id)

    @classmethod
    def getById( cls, gsid):
        """
        get GeneralSubmission by SID and validate SID
        """
        try:
            gsub = cls.objects.get(pk=gsid)
            return gsub

        except:
            raise Exception( cls.GENERAL_SUBMISSION_ID_NOT_EXIST.format(gsid))

    @classmethod
    def addGeneralSubmission( cls, user = None, problem = None, code_file_path = '', code_language = '', code_length = 0):
        """
        add GeneralSubmission, with user, problem, data_count, code_file_path, code_language, code_length
        """
        # use instances as params to omit the validation, cause validation has been done in vies
        # we should add validator in views module

        try:
            g_s = GeneralSubmission()
            other_info = {}
            g_s.user = user # user.submission_set.add may also be okay
            other_info['username'] = g_s.user.username

            g_s.problem = problem
            other_info['pid'] = g_s.problem_id

            g_s.status = 'Pending'
            other_info['status'] = g_s.status

            g_s.data_cnt = g_s.problem.data_count
            other_info['data_cnt'] = str(g_s.data_cnt)

            g_s.code_language = code_language
            other_info['code_language'] = g_s.code_language

            g_s.code_length = code_length
            other_info['code_length'] = str(g_s.code_length)

            g_s.run_time = 0
            other_info['run_time'] = str(g_s.run_time)
            g_s.run_memory = 0
            other_info['run_memory'] = str(g_s.run_memory)

            other_info['score'] = str(0)

            g_s.other_info = str(other_info)

            g_s.submission_time = datetime.now()

            g_s.save()
            flush_transaction()

            import os
            true_addr = os.path.join( Const.GENERAL_SUBMISSION_CODE_PATH, str(g_s.id))
            if default_storage.exists( true_addr): # bugs came out as versions updated
                default_storage.delete( true_addr)

            default_storage.save( true_addr, default_storage.open(code_file_path))
            # the second param is a FILE object or its subclass
            default_storage.delete( code_file_path)
            g_s.code_file = true_addr

            other_info = eval(g_s.other_info)
            other_info['code_file_path'] = g_s.code_file

            # cause we don't have it at former time
            other_info['submit_time'] = str(g_s.submission_time)

            g_s.other_info = str(other_info)

            g_s.save()
            flush_transaction()

            sent_to_queue = False
            while not sent_to_queue:
                try:
                    Core.tasks.JudgeQueue.sendJudge(_sid= g_s.id, _pid= g_s.problem_id, _lang= g_s.code_language,
                            _mode='general', _code_path=g_s.code_file)
                    sent_to_queue = True
                except Exception as e:
                    print str(e)

            return g_s.id

        except:
            raise

    @classmethod
    def rejudgeGeneralSubmission( cls, g_s):
        """
        func used to rejudge the very general submission
        """

        # no need to handle exception?
        # or exception transmission?

        try:
            info = eval(g_s.other_info)
            g_s.status = 'Rejudging'
            info['status'] = g_s.status
            g_s.run_time = 0
            info['run_time'] = str(g_s.run_time)
            g_s.run_memory = 0
            info['run_memory'] = str(g_s.run_memory)

            info['score'] = str(0)

            g_s.other_info = str(info)

            g_s.save()
            flush_transaction()

            sent_to_queue = False
            while not sent_to_queue:
                try:
                    Core.tasks.JudgeQueue.sendJudge(_sid= g_s.id, _pid= g_s.problem_id, _lang= g_s.code_language,
                            _mode='general', _code_path=g_s.code_file)
                    sent_to_queue = True
                except Exception as e:
                    print str(e)

            return True

        except:
            raise

    @classmethod
    def updateGeneralSubmission( cls, gsid, judge_info):
        """
        called by JudgeQueue
        save dict in other_info as str
        """

        try:
            s = cls.getById( gsid)

            print judge_info
            s.status = SUB_STATUS[judge_info['status']]
            #s.status = 'Accepted'

#debug 
            #s.save()
            #flush_transaction()

            info = eval( s.other_info)

            if s.status == 'Init':
                s.status = 'System Error'
                s.run_time = 0
                s.run_memory = 0
                info['run_time'] = str(s.run_time)
                info['run_memory'] = str(s.run_memory)
                info['case_judged'] = str(0)
                info['score'] = str(0)

            elif s.status == 'Compile Error':
                s.run_time = 0
                s.run_memory = 0
                info['run_time'] = str(s.run_time)
                info['run_memory'] = str(s.run_memory)
                info['ce'] = judge_info['ce']
                info['case_judged'] = str(0) 
                info['score'] = str(0)

            elif s.status != 'Compiling' and s.status != 'Judging':
                s.run_time = judge_info['time']
                s.run_memory = judge_info['mem']
                info['run_time'] = str(s.run_time)
                info['run_memory'] = str(s.run_memory)

                s.status = 'Judging'
                seq = []
                jd_cnt = 0
                case_dict = json.loads(s.problem.case_info)
                temp_score = 0

                for seq_res in judge_info['case_res']:
                    if jd_cnt >= judge_info['case_done']:
                        break

                    if seq_res['res'] == 're':
                        s.status = JUDGE_RES['re']
                    elif seq_res['res'] == 'mle':
                        s.status = JUDGE_RES['mle']
                    elif seq_res['res'] == 'tle':
                        s.status = JUDGE_RES['tle']
                    elif seq_res['res'] == 'wa':
                        s.status = JUDGE_RES['wa']
                    elif seq_res['res'] == 'pe':
                        s.status = JUDGE_RES['pe']
                    elif seq_res['res'] == 'ole':
                        s.status = JUDGE_RES['ole']

                    if seq_res['res'] == 'ac':
                        if not case_dict[str(jd_cnt)].isdigit():
                            raise Exception( "Invalid Score")
                        temp_score += int(case_dict[str(jd_cnt)])
                        seq_res['score'] = case_dict[str(jd_cnt)]

                    seq.append(seq_res)
                    jd_cnt += 1

                info['case_judged'] = judge_info['case_done']
                info['case_result'] = seq
                info['score'] = str(temp_score)
                if s.status == 'Judging':
                    s.status = 'Accepted'

            info['status'] = s.status

            s.other_info = str( info)
            s.save() # without such sentence, no data modification will be updated
            flush_transaction()

            return True

        except:
            raise

    @classmethod
    def generalSubmissionList( cls, u=None, p=None, uname=None, language=None, status_selected=None, university=None):
        """
        return the general submission list filter by params
        """

        try:
            g_sub = cls.objects.select_related('user', 'problem')
            if u:
                g_sub = g_sub.filter(user=u)
            if status_selected:
                g_sub = g_sub.filter(status=status_selected)
            if p:
                g_sub = g_sub.filter(problem=p)
            elif uname:
                g_sub = g_sub.filter(user__username__icontains=uname)
            if university:
                g_sub = g_sub.filter(user__university=university)
            if language:
                g_sub = g_sub.filter(code_language=language)
            g_sub = g_sub.order_by('-id')
            return g_sub

        except:
            raise

    @classmethod
    def generalSubmissionListOLD( cls, uid=None, pid=None, uname=None, language=None, status_selected=None):
        """
        return the general submission list filter by params
        """
        # use 'not' to judge None and ''
        # then no 'not' as True

        # and we should get pid by cid and p_index, so we have no need to use them here
        general_submissions = cls.objects.all()
        if pid:
            general_submissions = general_submissions.filter(problem_id=pid) # bugs fixed here, we should use __ instead of . to avoid using expression
        if uid:
            general_submissions = general_submissions.filter(user_id=uid)
        if uname:
            general_submissions = general_submissions.filter(user__username__icontains=uname) # omit CASE and search implicitly
        if language:
            general_submissions = general_submissions.filter(code_language=language)
        if status_selected:
            general_submissions = general_submissions.filter(status=status_selected)
        general_submissions = general_submissions.order_by('-id')
        num_submissions = general_submissions.count()
        # bugs here, logic uncorrect
        # pages = num_submissions / Const.STATUS_PER_PAGE + ( ( num_submissions % Const.STATUS_PER_PAGE) > 0)
        # page_id = min( max( 1, page_id), pages if pages > 0 else pages+1)
        # id_begin = ( page_id - 1) * Const.STATUS_PER_PAGE
        # id_end = min( page_id * Const.STATUS_PER_PAGE, num_submissions)
        return general_submissions#[id_begin:id_end]

    @classmethod
    def canViewCode( cls, g_sub, user):
        """
        if user could view code of the general_submission or not
        """

        try:
            if g_sub.user == user or user.priv == 'university':
                return True
            else:
                # fake
                # what's the priv of general problems?
                return False

        except:
            raise

    @classmethod
    def canSubmitCode( cls, user, p):
        """
        if user could submit some code to some very problem in general mode
        """
        # fake
        try:
            return p.canViewProblem( user)
        except:
            raise
