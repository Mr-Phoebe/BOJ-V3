# -.- encoding: utf-8 -.-

from django.db import models
from kari.const import Const
from User.models import User
from Contest.models import Contest, ContestProblem
from Submission.models import Submission
import json

# Create your models here.
class Board(models.Model):

    cuid = models.AutoField(primary_key=True)
    contest = models.ForeignKey('Contest.Contest')
    user = models.ForeignKey('User.User')
    status = models.TextField()

    def __unicode__(self):
        return self.status

    @classmethod
    def getById(cls, cu_id):
        try:
            return cls.objects.get(pk=cu_id)
        except Exception as e:
            raise e
        return False

    @classmethod
    def getByContest(cls, c):
        try:
            return cls.objects.filter(contest=c)
        except Exception as e:
            raise e
        return False

    @classmethod
    def getByContestAndUser(cls, c, u):
        try:
            return cls.objects.filter(contest=c).filter(user=u)
        except Exception as e:
            raise e
        return False

    @classmethod
    def addUserIntoContest(cls, u, c):
        try:
            newBoard = cls.getByContestAndUser(c, u)
            if newBoard==False:
                nB = Board()
                nB.contest = c
                nB.user = u
                nB.status = ""
                nB.save()
                return True
            return False
        except Exception as e:
            raise e
        return False

    @classmethod
    def removeUserFromContest(cls, u, c):
        try:
            nB = cls.getByContestAndUser(c, u)
            if nB==False:
                return False
            nB.delete()
            return True
        except Exception as e:
            raise e
        return False

    @classmethod
    def updateUserInContest(cls, u, c, s):
        try:
            nB = cls.getByContestAndUser(c, u)
            if nB==False:
                return False
            nB.status = s
            nB.save()
            return True
        except Exception as e:
            raise e
        return False

    @classmethod
    def init(cls, c):
        try:
            cls.objects.filter(contest=c).delete()
            return True
        except Exception as e:
            raise e
        return False

