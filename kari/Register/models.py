# coding: utf-8
from django.db import models
from hashlib import sha1, sha256
from Register.const import Const

class Contestant(models.Model):
    name        = models.CharField(max_length = Const.CONTESTANT_NAME_MAX_LENGTH)
    gender      = models.CharField(max_length = 10)
    email       = models.EmailField(null = True)
    grade       = models.CharField(max_length = 20)
    mobile      = models.CharField(max_length = Const.MOBILE_MAX_LENGTH)
    student_id  = models.CharField(max_length = Const.STUDENTID_MAX_LENGTH)
    class_id    = models.CharField(max_length = Const.CLASSID_MAX_LENGTH)
    school      = models.CharField(max_length = Const.SCHOOL_NAME_MAX_LENGTH)
    info        = models.CharField(max_length = 500)
    team        = models.ForeignKey('Team')

    def __unicode__(self):
        return str(self.pk) + ' ' + self.name

    def _checkInfo(self):
        # Check Name
        if len(self.name) < Const.CONTESTANT_NAME_MIN_LENGTH or len(self.name) > Const.CONTESTANT_NAME_MAX_LENGTH:
            raise Exception(u'姓名不合法！')

        # Check Email
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        try:
            validate_email(self.email)
        except ValidationError:
            raise Exception(u'Email不合法！')

        # Check IDs
        validSet = "0123456789"
        for token in self.student_id:
            if not token in validSet:
                raise Exception(u'学号不合法！')
        for token in self.class_id:
            if not token in validSet:
                raise Exception(u'班级不合法！(请输入10位班级编号)')
        
        # Check whether the team has been full
        members = Contestant.objects.filter(team = self.team)
        if len(members) >= 1:
            raise Exception(u'您已经完善过信息了！')

        return True

    def _checkModifyInfo(self):
        # Check Name
        if len(self.name) < Const.CONTESTANT_NAME_MIN_LENGTH or len(self.name) > Const.CONTESTANT_NAME_MAX_LENGTH:
            raise Exception(u'姓名不合法！')

        # Check Email
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        try:
            validate_email(self.email)
        except ValidationError:
            raise Exception(u'Email不合法！')

        # Check IDs
        validSet = "0123456789"
        for token in self.student_id:
            if not token in validSet:
                raise Exception(u'学号不合法！')
        for token in self.class_id:
            if not token in validSet:
                raise Exception(u'班级不合法！(请输入10位班级编号)')

        return True

    @classmethod
    def getAllContestant(cls):
        return cls.objects.all()
    
    @classmethod
    def delAllContestant(cls):
        try:
            cls.objects.all().delete()
        except Exception as e:
            raise e

    @classmethod
    def getById(cls, request_id):
        return cls.objects.get(pk = request_id)

    @classmethod
    def getByName(cls, request_name):
        return cls.objects.get(name = request_name)

    @classmethod
    def getTeamContestant(cls, request_team):
        try:
            result = cls.objects.filter(team = request_team)
        except:
            result = []
        return result

    @classmethod
    def addContestant(cls, name, gender, grade, email, mobile, student_id, class_id, school, info, team):
        try:
            c = Contestant()
            c.name = name
            c.gender = gender
            c.grade = grade
            c.email = email
            c.mobile = mobile
            c.student_id = student_id
            c.class_id = class_id
            c.school = school
            c.info = info
            c.team = team
            c._checkInfo()
            c.save()
            return c
        except Exception as e:
            raise e
    
    def modifyContestant(self, name, gender, grade, email, mobile, student_id, class_id, school, info, team):
        try:
            self.name = name
            self.gender = gender
            self.grade = grade
            self.email = email
            self.mobile = mobile
            self.student_id = student_id
            self.class_id = class_id
            self.school = school
            self.info = info
            self.team = team
            self._checkModifyInfo()
            self.save()
            return self
        except Exception as e:
            raise e

class Team(models.Model):
    name    = models.CharField(max_length = Const.TEAM_NAME_MAX_LENGTH, unique = True)
    passwd  = models.CharField(max_length = 128)
    status  = models.CharField(max_length = 30)
    reason  = models.TextField()

    def __unicode__(self):
        return str(self.pk) + ' ' + self.name

    def _encodePasswd(self):
        newPasswd = sha1(str(self.passwd)).hexdigest()
        newPasswd = sha256(newPasswd + Const.PASSWD_SALT).hexdigest()
        self.passwd = newPasswd
        self.save()

    def matchPasswd(self, pswd):
        encedPasswd = sha1(str(pswd)).hexdigest()
        encedPasswd = sha256(encedPasswd + Const.PASSWD_SALT).hexdigest()
        if encedPasswd == self.passwd:
            return True
        else:
            raise Exception(u'Password doesn\'t match')
    
    def resetPasswd(self, pswd):
        try:
            # Check Raw Password
            self.passwd = pswd
            if len(self.passwd) < Const.PASSWD_MIN_LENGTH or len(self.passwd) > Const.PASSWD_MAX_LENGTH:
                raise Exception(u'密码长度应在%s到%s之间！' % (Const.PASSWD_MIN_LENGTH, Const.PASSWD_MAX_LENGTH))
            self._encodePasswd() 
            self.save()
            return self
        except Exception as e:
            raise e
    
    def updateStatus(self, status):
        self.status = status
        self.save()
        return self

    def _checkInfo(self):
        # Check Name
        if len(self.name) < Const.TEAM_NAME_MIN_LENGTH or len(self.name) > Const.TEAM_NAME_MAX_LENGTH:
            raise Exception(u'ID不合法！')
        for token in self.name:
            if token == ' ':
                raise Exception(u'ID不能包含空格')

        flag = True
        try:
            t = Team.getByName(self.name)
            flag = False
        except:
            pass
        if not flag:
            raise Exception(u'此ID已经被注册！')

        # Check Raw Password
        if len(self.passwd) < Const.PASSWD_MIN_LENGTH or len(self.passwd) > Const.PASSWD_MAX_LENGTH:
            raise Exception(u'密码长度应在%s到%s之间！' % (Const.PASSWD_MIN_LENGTH, Const.PASSWD_MAX_LENGTH))
        return True

    @classmethod
    def getByName(cls, request_name):
        return cls.objects.get(name = request_name)

    @classmethod
    def getById(cls, request_id):
        request_id = int(request_id)
        try:
            return cls.objects.get(pk = request_id)
        except:
            raise Exception(u'没有编号为%s的队伍！' % request_id)

    @classmethod
    def getSessionTeam(cls, session):
        try:
            if not 'team_id' in session:
                raise
            return cls.getById(session['team_id'])
        except Exception as e:
            raise Exception(u'No logged-in team in current session')

    @classmethod
    def getAllTeams(cls):
        return cls.objects.all()
   
    @classmethod
    def getMaxId(cls):
        maxx = 1
        for t in cls.objects.all():
            maxx = max(maxx, t.pk)
        return maxx

    @classmethod
    def getPendingTeams(cls):
        return cls.objects.filter(status = 'Pending')

    @classmethod
    def addTeam(cls, name, passwd):
        try:
            t = Team()
            t.name = name
            t.passwd = passwd
            t._checkInfo()
            t._encodePasswd()
            t.status = 'Pending'
            t.save()
            return t
        except Exception as e:
            raise e

    @classmethod
    def delAllTeam(cls):
        try:
            cls.objects.all().delete()
        except Exception as e:
            raise e
