# coding: utf-8

from django.db import models
from hashlib import sha1, sha256
from kari.const import Const
from django.core.exceptions import ValidationError
from django.db.models import Q
import random
import csv

class User(models.Model):
    uid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=Const.USERNAME_MAX_LENGTH,
                                unique=True)
    nickname = models.CharField(max_length=Const.NICKNAME_MAX_LENGTH)
    passwd = models.CharField(max_length=128)
    email = models.EmailField(max_length=Const.EMAIL_MAX_LENGTH, null=True,  unique=True)
    gender = models.CharField(max_length=6,
                              choices=Const.GENDER_CHOICE,
                              default='secret')
    preferred_lang = models.CharField(max_length=20,
                                      choices=Const.LANG,
                                      default='g++')
    #last_ip = models.GenericIPAddressField()
    priv = models.CharField(max_length=15,
                            choices=Const.USER_PRIV_CHOICE)
    #foreign key
    #
    university = models.ForeignKey('University')
    school = models.ForeignKey('School', null=True, blank=True)

    class Meta:
        index_together = [
            ['university', 'priv'],
            ['university', 'school'],
        ]

    def __unicode__(self):
        return self.username
    
    def isCourseClassAdmin(self):
        if self.priv == 'courseclass':
            return True
        return False
    def isStudent(self):
        if self.priv == 'student':
            return True
        return False

    def _encPasswd(self):
        newPasswd = sha1(str(self.passwd)).hexdigest()
        newPasswd = sha256(newPasswd + Const.PASSWD_SALT).hexdigest()
        self.passwd = newPasswd
        self.save()

    def _chkPasswd(self, pswd):
        encedPasswd = sha1(str(pswd)).hexdigest()
        encedPasswd = sha256(encedPasswd + Const.PASSWD_SALT).hexdigest()
        return encedPasswd == self.passwd

    def _vUsername(self):
        legalChSet = 'qwertyuioplkjhgfdsazxcvbnm1234567890_'
        for ch in self.username:
            if not ch in legalChSet:
                raise Exception('username illegal')
        if len(self.username)<Const.USERNAME_MIN_LENGTH or len(self.username)>Const.USERNAME_MAX_LENGTH:
            raise Exception('username illegal')

    def _vRawPasswd(self):
        if len(self.passwd)<Const.PASSWD_MIN_LENGTH or len(self.passwd)>Const.PASSWD_MAX_LENGTH:
            raise Exception('passwd illegal')

    def _vNickname(self):
        if len(self.nickname)<0 or len(self.nickname)>Const.NICKNAME_MAX_LENGTH:
            raise Exception('nickname illegal')

    def _vEmail(self):
        if self.email == None:
            return True
        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError
        try:
            validate_email(self.email)
        except ValidationError:
            raise Exception('email illegal')

    def checkPasswd(self, passwd):
        return self._chkPasswd(passwd)
    
    def update(self, nk, ps, em, gd):
        self.nickname = nk
        self.passwd = ps
        self.email = em
        self.gender = gd

        self._vNickname()
        self._vRawPasswd()
        self._vEmail()

        self._encPasswd()
        self.save()

    def updateNoPass(self, nk, em, gd):
        self.nickname = nk
        self.email = em
        self.gender = gd

        self._vNickname()
        self._vEmail()

        self.save()

    def belongsToGroup(self, group):
        if self in group.users.all():
            return True
        return False

    def addAdmin(self, name, passwd, prvlg):
        if self.priv != 'university':
            raise Exception('no priv')
        return User.addUser(name, passwd, self.university, prvlg)

    def csvGenerate(self,succ):
        name = self.username
        name = name.replace('#','_')
        csvfile = file('/tmp/%s.csv'%name,'wb')
        writer = csv.writer(csvfile)
        writer.writerow(['用户名','密码'])
        for (name,psw) in succ.items():
            writer.writerow([name,psw])
        csvfile.close()

    @classmethod
    def addUser(cls, username, passwd, university, prvlg='student', nickname='', email=None):
        u = User()
        univ_name = university.name
        u.username = username
        u._vUsername()
        u.username = univ_name+'#'+username
        u.passwd = passwd
        u.university = university
        u._vRawPasswd()
        u._encPasswd()
        u.email = email
        u._vEmail()
        u.priv = prvlg
        u.nickname = nickname
        u.save()
        return u

    @classmethod
    def _genRandPasswd(cls, length=8):
        candidates = 'qwertyupasdfghjkzxcvbnm23456789'
        return ''.join(random.sample([x for x in candidates], length))
    
    def ResetPasswd(self, mode):
        if mode == 'random':
            newpasswd = User._genRandPasswd()
        elif mode == 'username':
            newpasswd = self.username.split('#')[1]
        else:
            raise Exception('mode illegal')
        self.passwd = newpasswd
        self._encPasswd()
        self.save()
        return newpasswd

    @classmethod
    def getUserByRawUsername(cls, usname):
        try:
            u = User.objects.get(username=usname)
        except:
            return False
        return u

    @classmethod
    def getSessionUser(cls, session):
        if 'uid' in session:
            try:
                return User.objects.get(pk=session['uid'])
            except:
                return False
        else:
            return False

    @classmethod
    def getById( cls, u_id):
        """
        get User by ID, and validation
        """
        try:
            user = cls.objects.get(pk=u_id)
        except:
            raise Exception( 'No such User with ID {0}'.format( u_id))
        
        return user

    @classmethod
    def listUserByPriv( cls, privilege, univ=None, sch=None):
        """
        list users priv
        """
        
        users = User.objects.filter(
                Q( university=univ),
                Q( priv=privilege),
                Q( school=sch) | Q( school=None),
                )
            
        return users

class School(models.Model):
    fullname = models.CharField(max_length=Const.SCHOOLNAME_MAX_LENGTH)
    name = models.CharField(max_length=Const.SCHOOLABBR_MAX_LENGTH,
                            unique=True)
    admin = models.ForeignKey('User', related_name='schools', null=True, blank=True)
    university = models.ForeignKey('University')

    def __unicode__(self):
        return self.name

    @classmethod
    def addSchool(cls, schname, schfname, univ):
        s = School(name=schname, fullname=schfname, university=univ)
        s.save()
        return s

    @classmethod
    def getSchoolsByAdmin( cls, user):
        """
        return school(s) managed by the very admin
        """
        return cls.objects.filter( admin=user)

    @classmethod
    def getById(cls, sch_id):
        """
        get School by ID, and validation
        """
        try:
            school = cls.objects.get(pk=sch_id)
        except:
            raise Exception( 'No such School with ID {0}'.format( sch_id))
        
        return school
    
    def isAdmin(self, user):
        if user.priv == 'school' and self.admin == user:
            return True
        return False

    @classmethod
    def validSchoolname(cls, sname):
        return len(sname) > 0 and len(sname) < 50

    @classmethod
    def validSchoolabbr(cls, sabbr):
        return len(sabbr) > 0 and len(sabbr) < 50

class Group(models.Model):
    name = models.CharField(max_length=Const.GROUPNAME_MAX_LENGTH,
                                 unique=True)
    users = models.ManyToManyField('User')
    school = models.ForeignKey('School')
    def __unicode__(self):
        return self.name
    def allMembers(self):
        return self.users.select_related('university')
    def addMember(self, user):
        self.users.add(user)
        self.save()
    def delMember(self, user):
        if user in self.users.all():
            self.users.remove(user)
        else:
            raise Exception(Const.USER_NOT_IN_GROUP)

    def validGroupname(self):
        if len(self.name) < Const.GROUPNAME_MIN_LENGTH or len(self.name) > Const.GROUPNAME_MAX_LENGTH:
            raise Exception('groupname illegal')

    @classmethod
    def addGroup(cls, groupname, sch):
        g = Group(name=groupname, school=sch)
        g.validGroupname()
        g.save()
        return g

    @classmethod
    def getById( cls, grp_id):
        """
        get Group by ID, and validation
        """
        try:
            group = cls.objects.get(pk=grp_id)
        except:
            raise Exception( 'No such Group with ID {0}'.format( grp_id))
        
        return group

class University(models.Model):
    name = models.CharField(max_length=Const.UNIVNAME_MAX_LENGTH,
                            unique=True)
    fullname = models.CharField(max_length=Const.UNIVABBR_MAX_LENGTH)
    admin = models.ForeignKey('User', related_name='univs', null=True, blank=True)
    def __unicode__(self):
        return self.name

    @classmethod
    def addUniversity(cls, uniname):
        un = University(name=uniname, fullname=uniname)
        un.save()
        return un

    @classmethod
    def getById( cls, univ_id):
        """
        get University by ID, and validation
        """
        try:
            university = cls.objects.get(pk=univ_id)
        except:
            raise Exception( 'No such University with ID {0}'.format( univ_id))
        
        return university

    @classmethod    
    def getByName(cls, univ_name):
        try:
            university = cls.objects.get(name = univ_name)
        except:
            raise Exception('No such University with Name {0}'.format(univ_name))
        return university

    def isAdmin(self, user):
        if user.priv == 'university' and self.admin == user:
            return True
        return False
