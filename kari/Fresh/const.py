# coding: utf-8

class Const():
    """
    Team
    """
    TEAM_NAME_MIN_LENGTH = 1
    TEAM_NAME_MAX_LENGTH = 30
    TEAM_STATUS = ('Pending', 'Accepted', 'Failed', 'Skipped', 'Starred', 'Finals')

    """
    Contestant
    """
    CONTESTANT_NAME_MIN_LENGTH = 1
    CONTESTANT_NAME_MAX_LENGTH = 20
    MOBILE_MIN_LENGTH = 10
    MOBILE_MAX_LENGTH = 11
    STUDENTID_MIN_LENGTH = 8
    STUDENTID_MAX_LENGTH = 11
    CLASSID_MIN_LENGTH = 8
    CLASSID_MAX_LENGTH = 11
    SCHOOL_NAME_MIN_LENGTH = 1
    SCHOOL_NAME_MAX_LENGTH = 50
    PASSWD_MIN_LENGTH = 6
    PASSWD_MAX_LENGTH = 30
    PASSWD_SALT = "j#$E&s(SI$e$sZ^^e*F%aN!yin#D+&I=r)&A"

    PRIVILEGE_CHOICE = (('contestant', 'contestant'), ('admin', 'admin'))

    GENDER_CHOICES = (u'男', u'女')
    SCHOOL_CHOICES = (u'信息与通信工程学院', u'计算机学院', u'软件学院', u'自动化学院', u'经管学院', u'理学院', u'电子工程学院', u'语言学院', '人文学院', u'国际学院', u'网研院', u'光研院', u'其他学院')
    GRADE_CHOICES  = (u'大一', u'大二', u'大三', u'大四', u'研一', u'研二', u'研三')

    """
    Admin
    """
    ADMIN_KEY = 'bupticpc@912'
