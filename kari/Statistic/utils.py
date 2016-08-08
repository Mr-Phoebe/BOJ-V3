# -.- encoding: utf-8 -.-

from Problem.models import Problem
from User.models import User
from django.http import HttpResponse
from hashlib import md5
from django.shortcuts import render_to_response, render, redirect
from kari.const import Const
from Problem.forms import addProblemForm
from django.core.files.storage import default_storage
from Contest.models import ContestProblem, Contest
from Statistic.models import Board
from Submission.models import Submission
import os
import json
from django.core.cache import cache

#f = open('/home/buptacm/log.txt', 'w')

#def debug(s):
#    print >> f, s

def getSBC(c):
    ckey = 'Submission_csbc' + str(c.pk)

    sub_all = cache.get(ckey)
#    with open('/home/buptacm/log2.txt', 'w') as f2:
#        print >> f2, sub_all
    if sub_all == None:
        sub_all = Submission.submissionList(c=c)
        cache.set(ckey,sub_all,Const.CACHE_TIME_FIRST)
        #cache.set(ckey,sub_all,15)
    return sub_all
"""
def getSUB():
    ckey = 'submissions'
    sub = cache.get(ckey)
    if sub == None:
        sub = Submission
        cache.set(ckey,sub,10)
    return sub
"""

"""
def bigfilter( u=None, c=None, cp=None, uname=None, lang=None, sta=None, board_stop_time=None):

    try:
        ckey = 'submissions'
        s = cache.get(ckey)
        if s == None:
            s = Submission.objects.select_related('user', 'problem_index').filter(problem_index__contest=c)
            cache.set(ckey,s,10)
        if sta:
            s = s.filter(status=sta)
        if cp:
            s = s.filter(problem_index=cp)
        elif c:
            s = s.filter(problem_index__contest=c)
        else:
            raise Exception('evil query')
        if u:
            s = s.filter(user=u)
        elif uname:
            s = s.filter(user__username__icontains=uname)
        if lang:
            s = s.filter(code_language=lang)
        if board_stop_time:
            s = s.filter(submission_time__lt=board_stop_time)
        s = s.order_by('-sid')
        return s
        
    except:
        raise
"""


def getContestResult(c):
    try:
        allSub = getSBC(c=c)
        allProb = c.getContestProblem()

        ac_cnt={}
        sub_cnt={}
        for pinfo in allProb:
            ac_cnt[pinfo.problem_index]=0
            sub_cnt[pinfo.problem_index]=0
        
        for sinfo in allSub:
            if sinfo.status == "Accepted":
                ac_cnt[sinfo.problem_index.problem_index]+=1
            sub_cnt[sinfo.problem_index.problem_index]+=1
        res=[]
        for pinfo in allProb:
            tdict={}
            tdict["ac_cnt"]=ac_cnt[pinfo.problem_index]
            tdict["sub_cnt"]=sub_cnt[pinfo.problem_index]
            if sub_cnt[pinfo.problem_index] == 0:
                tdict["ac_ratio"]=0.00
            else:
                tdict["ac_ratio"]=round(ac_cnt[pinfo.problem_index]*100.0/sub_cnt[pinfo.problem_index],2)
            res.append(tdict)
        return res
    except Exception as e:
        return []

def getContestUserResult(c, u):
    try:
        allSub = getSBC(c=c)
        allProb = c.getContestProblem()
        ac_cnt={}
        for pinfo in allProb:
            ac_cnt[pinfo.problem_index]=0
        
        for sinfo in allSub:
            if u != sinfo.user:
                continue
            if sinfo.status == "Accepted":
                ac_cnt[sinfo.problem_index.problem_index] = 1
        res=[]
        for pinfo in allProb:
            res.append(ac_cnt[pinfo.problem_index])
        return res
    except Exception as e:
        return []

