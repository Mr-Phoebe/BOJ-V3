# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime, timedelta
from kari.const import Const
from Problem.models import Problem
from User.models import User
from Course.models import CourseClass

class Contest(models.Model):
    """
    Contest information
    """

    TITLE_MIN_LEN = 1
    TITLE_MAX_LEN = 128

    cid = models.AutoField(primary_key=True)
    contest_title = models.CharField(max_length=TITLE_MAX_LEN)
    contest_description = models.TextField(default='')
    start_time = models.DateTimeField()
    length = models.IntegerField(default=300)  # default is 5 hours
    board_stop = models.IntegerField(default=300)  # default is 5 hours, means board won't stop
    author = models.ForeignKey('User.User')
    course_class = models.ForeignKey('Course.CourseClass')
    contest_type = models.IntegerField(default=0)  # 0 for public
    board_type = models.IntegerField(default=0)  # 0 for ACM board, 1 for Scroing board, 2 for submit only(submissions won't be judged and will be
                                                 # set to "AC" directly).
    lang_limit = models.IntegerField(default=0)  # mask

    def __unicode__(self):
        return self.contest_title

    def _vTitle(self):
        if len(self.contest_title) < self.TITLE_MIN_LEN or len(self.contest_title) > self.TITLE_MAX_LEN:
            raise Exception(Const.CONTEST_TITLE_ERR)

    def _vStartTime(self):
        if self.start_time <= datetime.now():
            raise Exception(Const.CONTEST_TIME_ERR)

    def _vLength(self):
        if self.length <= 0:
            raise Exception(Const.CONTEST_LEN_ERR)

    def _vBoardStop(self):
        if self.board_stop <= 0:
            raise Exception(Const.CONTEST_BOARD_ERR)
    
    def isPermittedLang(self, lang):
        return Const.LANG_MASK[lang] & self.lang_limit != 0
    
    def permittedLangs(self):
        return filter(self.isPermittedLang, Const.LANG_MASK.keys())

    @classmethod
    def getById(cls, contestId):
        try:
            return Contest.objects.get(cid=contestId)
        except:
            raise Exception(Const.CONTEST_NOT_EXIST)
        
    @classmethod
    def getByAdmin(cls, user):
        cList = []
        ccList = CourseClass.getAllManagedClasses(user)
        map(cList.extend, [Contest.getByCourseClass(cc) for cc in ccList])
        cList = list(set(cList))
        return sorted(cList, key=lambda contest: contest.start_time, reverse=True)
    
    @classmethod
    def getByAuthor(cls, user):
        return Contest.objects.filter(author=user).order_by('-start_time')

    @classmethod
    def getByCourseClass(cls, courseClass):
        return Contest.objects.filter(course_class=courseClass).order_by('-start_time')
        
    @classmethod
    def getByStudent(cls, user):
        cList = []
        map(cList.extend, [Contest.getByCourseClass(cc) for cc in CourseClass.getByStudent(user)])
        cList = list(set(cList))
        return sorted(cList, key=lambda contest: contest.start_time, reverse=True)

    @classmethod
    def getByUniversity(cls, uni):
        #return Contest.objects.all()
        all_user = User.objects.filter(university=uni)
        return Contest.objects.filter(author__in = all_user).order_by('-start_time')

    @classmethod
    def addContest(cls, user, courseClass, contestTitle, pInfos, startTime, contestDesc='',
                   length=300, boardStop=300, contestType=0, boardType=0, lang_limit=0):

        # add contest now
        c = Contest()
        c.author = user
        c.course_class = courseClass
        c.contest_title = contestTitle
        c._vTitle()
        c.start_time = startTime
        c._vStartTime()
        c.length = length
        c._vLength()
        c.board_stop = boardStop
        c._vBoardStop()
        c.contest_description = contestDesc
        c.contest_type = contestType
        c.board_type = boardType
        c.lang_limit = lang_limit
        c.save()

        # add problem to contest now
        for pInfo in pInfos:
            contestProb= ContestProblem()
            contestProb.contest = c
            try:
                contestProb.problem = Problem.objects.get(pid=pInfo[0])
            except:
                raise Exception(Const.CONTEST_PROB_ERR)
            if not Problem.isLegalTitle(pInfo[1]) or len(pInfo[1]) == 0:
                contestProb.problem_title = contestProb.problem.prob_title
            else:
                contestProb.problem_title = pInfo[1]
            contestProb.problem_index = pInfo[2]
            contestProb.save()

        return c

    def updateContest(self, contestTitle, pInfos, startTime, contestDesc='', length=300,
                      boardStop=300, contestType=0, boardType=0, lang_limit=0):
        self.contest_title = contestTitle
        self._vTitle()
        if self.start_time != startTime:
            self.start_time = startTime
            self._vStartTime()
        self.length = length
        self._vLength()
        self.board_stop = boardStop
        self._vBoardStop()
        self.contest_description = contestDesc
        self.contest_type = contestType
        self.board_type = boardType
        self.lang_limit = lang_limit
        self.save()
       
        # To be modified, URGENT
        try:
            self._vStartTime()
        except:
            return True

        map(lambda x:x.delete(), ContestProblem.objects.filter(contest=self))
        
        for pInfo in pInfos:
            try:
                prob = Problem.objects.get(pid=pInfo[0])
            except:
                raise Exception(Const.CONTEST_PROB_ERR)
##            try:
##                contestProb = ContestProblem.objects.get(contest=self, problem=prob)
##            except:
##                contestProb = ContestProblem()
##                contestProb.contest = self
##                contestProb.problem = prob
            contestProb = ContestProblem()
            contestProb.contest = self
            contestProb.problem = prob

            if not Problem.isLegalTitle(pInfo[1]) or len(pInfo[1]) == 0:
                contestProb.problem_title = contestProb.problem.prob_title
            else:
                contestProb.problem_title = pInfo[1]
            contestProb.problem_index = pInfo[2]
            contestProb.save()

        return True
    
    def addNotice(self, title, content=''):
        cn = ContestNotice()
        cn.contest = self
        cn.notice_title = title
        cn._vTitle()
        cn.notice_content = content
        cn.time = datetime.now()
        cn.save()
        return cn        
    
    def isScoringBoard(self):
        return self.board_type != 0

    def countContestProblem(self):
        return ContestProblem.objects.filter(contest=self).count()

    def getContestProblem(self):
        return ContestProblem.objects.filter(contest=self).order_by('problem_index')
    
    def getContestNotice(self):
        return ContestNotice.objects.filter(contest=self)

    @classmethod
    def canTouchContest(cls, courseClass, userObj):
        if courseClass.canBeAccessed(userObj):
            return True
        raise Exception(Const.NOT_PVLG)
        
    def canEnterContest(self, userObj):
        cc = self.course_class
        return Contest.canTouchContest(cc, userObj)

    def canEnterWithTime(self, user):
        if self.course_class.canBeAccessed(user) and datetime.now()>self.start_time:
            return True
        else:
            return False
    
    def canEnter(self, user):
        if not user:
            return False
        try:
            if self.canEnterContest(user):
                return True
            return False
        except:
            try:
                if self.canBeManaged(user):
                    return True
                return False
            except:
                return False
        return False

    @classmethod
    def hasPriv(cls, courseClass, userObj):
        return courseClass.canBeManaged(userObj)
    
    @classmethod
    def canAddContest(cls, courseClass, userObj):
        if courseClass.canBeManaged(userObj):
            return True
        raise Exception(Const.NOT_PVLG)
        
    def canBeManaged(self, userObj):
        if self.course_class.canBeManaged(userObj):
            return True
        raise Exception(Const.NOT_PVLG)
        
    def _canBeManaged(self, userObj):
        if self.course_class.canBeManaged(userObj):
            return True
        else:
            return False
        
    def isAdmin(self, userObj):
        return self.course_class.isAdmin(userObj)
    
    def isStarted(self, deltaMin=0):
        now = datetime.now() + timedelta(minutes=deltaMin)
        return now > self.start_time
        
    def isEnded(self):
        now = datetime.now()
        left = max(0, int((self.start_time + timedelta(minutes=self.length) - now).total_seconds())/60)
        return left == 0
    
class ContestProblem(models.Model):
    """
    Problem information in Contest
    """
    
    contest = models.ForeignKey('Contest')
    problem = models.ForeignKey('Problem.Problem')
    problem_title = models.CharField(max_length=128)
    problem_index = models.CharField(max_length=2)

    def __unicode__(self):
        return self.problem_index+'. '+self.problem_title

    @classmethod
    def getBy(cls, c, idx):
        try:
            return ContestProblem.objects.get(contest=c, problem_index=idx)
        except:
            raise Exception(Const.CONTEST_PROB_NOT_EXIST)

    @classmethod
    def getByContestAndProblemIndex(cls, cId, idx):
        try:
            c = Contest.getById(cId)
            return ContestProblem.objects.get(contest=c, problem_index=idx)
        except:
            raise Exception(Const.CONTEST_PROB_NOT_EXIST)

    def getScore(self):
        from Submission.models import Submission
        acUserCount = Submission.submissionList(cp=self).filter(status='Accepted').values('user').distinct().count()
        allUser = self.contest.course_class.getAllStudents()

        # eliminate users not in this contest, eg: admin
        allUidWithSubmission = set([u['user'] for u in Submission.submissionList(c=self.contest).values('user')])
        userWithSubmissionCount = len(filter(lambda u: u.uid in allUidWithSubmission, allUser))
        score = 0
        while acUserCount <= userWithSubmissionCount and score != 3000:
            score += 500
            acUserCount *= 2
        return score

            
class ContestNotice(models.Model):
    """
    Problem information in Contest
    """

    TITLE_MIN_LEN = 1
    TITLE_MAX_LEN = 128

    contest = models.ForeignKey('Contest')
    notice_title = models.CharField(max_length=TITLE_MAX_LEN)
    notice_content = models.TextField()
    time = models.DateTimeField()

    def _vTitle(self):
        if len(self.notice_title) < self.TITLE_MIN_LEN or len(self.notice_title) > self.TITLE_MAX_LEN:
            raise Exception(Const.CONTEST_NOTICE_TITLE_ERR)
    
    @classmethod
    def getById(cls, cnId):
        try:
            return ContestNotice.objects.get(pk=cnId)
        except:
            raise Exception(Const.CONTEST_NOTICE_NOT_EXIST)
        
    def updateNotice(self, title, content=''):
        self.notice_title = title
        self._vTitle()
        self.notice_content = content
        self.save()        
        return True
        
class Clarification(models.Model):
    """
    Q&A in contest
    """

    author      = models.ForeignKey('User.User')
    contest     = models.ForeignKey('Contest')
    question    = models.TextField()
    answer      = models.TextField()

    def __unicode__(self):
        return self.question

    def _checkQuestion(self):
        if len(self.question) == 0:
            raise Exception('Invalid Clarification')
        return True

    def _checkContest(self):
        if self.contest == None:
            raise Exception('Invalid Contest')

    def _checkAuthor(self):
        try:
            if self.author == None:
                raise
            if not self.contest.canEnterContest(self.author):
                raise
            return True
        except:
            raise Exception('Invalid Author')

    @classmethod
    def addClarification(cls, question, author, contest):
        try:
            c = Clarification()
            c.question = question
            c.author = author
            c.contest = contest
            c.answer = ''
            c._checkQuestion()
            c._checkContest()
            c._checkAuthor()
            c.save()
            return c
        except Exception as e:
            raise e
   
    @classmethod
    def getByContestId(cls, cid):
        cs = cls.objects.filter(contest__cid = cid)
        return cs

    @classmethod
    def getById(cls, cid):
        cs = cls.objects.get(pk = cid)
        return cs

    def updateAnswer(self, answer, user):
        try:
            if not self.contest or not user:
                raise
            self.contest.canBeManaged(user)
            self.answer = answer;
            self.save()
            return self
        except:
            raise Exception('Update answer failed')
   
    def deleteClarification(self):
        self.contest = Contest.getById(10)
        self.save()

    def canBeAccessed(self, user):
        c = self.contest
        if not c or not user:
            return False
        try:
            if c.canBeManaged(user):
                return True
        except:
            try:
                if c.canEnterContest(user):
                    return True
                return False
            except:
                return False
        return False

    def canBeManaged(self, user):
        if not user:
            return False
        if not self.contest.canBeManaged(user):
            return False
        return True
