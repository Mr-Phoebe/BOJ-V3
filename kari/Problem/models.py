# -.- encoding: utf-8 -.-

from django.db import models
from kari.const import Const
from User.models import *
from Course.models import Course, CourseClass
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.core.files.base import File, ContentFile
import json
import os

class Problem(models.Model):

    TITLE_MAX_LEN = 128
    DESC_MAX_LEN = 32768
    ADMIN_ID = 0

    TITLE_ERRMSG = u'长度最长128字符'
    DESC_ERRMSG = u'长度最长32768字符'
    PRV_ERRMSG = u'你没有权限'
    PID_ERRMSG = u'没有这个题目'
    LIST_PROBLEM_ERRMSG = u'没有这个页面'
    INPUT_ERRMSG = u'输入数据错误'

    #problem privilege
    PROB_PRIV_CH = (
            ('private','private'),  #only the author may view and modify it outside the contest
            ('protected','protected'),  #the admin with the same root as the author may view and modify it
            ('public','public'),  #the admin with the same root as the author may view and modify it, with all user may view it outside
            ('ext','ext'),  #more complex privilege
            #if more complex privilege needed, you may add it here
            )

    #problem info
    #
    pid = models.AutoField(primary_key=True)
    prob_priv = models.CharField(max_length=10, choices=PROB_PRIV_CH) 
    prob_title = models.CharField(max_length=TITLE_MAX_LEN, default='Untitled')
    prob_time = models.IntegerField(default=1000) #time limit in ms
    prob_memory = models.IntegerField(default=32768) #memory limit in kb
    prob_codelength = models.IntegerField(default=65536) #code len limit?
    #prob_desc = models.CharField(max_length=DESC_MAX_LEN)
    prob_desc = models.TextField() #xml description
    is_spj = models.IntegerField(default=0) # 0: no spj; 1: all data spj
    #spj = models.IntegerField() # 0: no spj; 1: all data spj
    # I think int is more flexible   --- Tom
    #uid = models.IntegerField() # author's user id
    author = models.ForeignKey('User.User')
    data_count = models.IntegerField(default=0) # number of test data
#    prob_tag = models.TextField() #Tag of the problem
#    prob_sub = models.IntegerField(default=0) #submittion number
#    prob_ac = models.IntegerField(default=0) #accepted number
    course = models.ForeignKey('Course.Course', blank=True, null=True, default=None)
    case_info = models.TextField()

    def __unicode__(self):
        return self.prob_title

    @classmethod
    def getById(cls, p_id):
        try:
            return cls.objects.get(pk=p_id)
        except Exception as e:
            raise e

    @classmethod
    def isLegalTitle(cls,title):
        return len(title) < cls.TITLE_MAX_LEN

    @classmethod
    def _isLegalDesc(cls,desc):
        return len(desc) < cls.DESC_MAX_LEN

    def copyProblemFromID(self, source_problem_id):
        # Warning: the function will delete all old test data of the problem itself
        try:
            source = Problem.getById(source_problem_id)
            self.prob_priv          = source.prob_priv
            self.prob_title         = source.prob_title
            self.prob_time          = source.prob_time
            self.prob_memory        = source.prob_memory
            self.prob_codelength    = source.prob_codelength
            self.prob_desc          = source.prob_desc
            self.is_spj             = source.is_spj
            self.author             = source.author
            self.data_count         = source.data_count
            self.course             = source.course
            self.case_info          = source.case_info
            self.save()

            dest_dir = Const.PROBLEM_DATA_PATH + str(self.pid) + '/'
            src_dir = Const.PROBLEM_DATA_PATH + str(source_problem_id) + '/'
            
            for file_list in default_storage.listdir(dest_dir): # Delete the old test data
                for files in file_list:
                    path = dest_dir + files
                    if default_storage.exists(path):
                        default_storage.delete(path)

            for data_id in xrange(self.data_count):             # Copy the test data
                dest_path = dest_dir + str(data_id) + '.in'
                src_path = src_dir + str(data_id) + '.in'
                if default_storage.exists(dest_path):
                    default_storage.delete(dest_path)
                new_file = default_storage.open(src_path)
                default_storage.save(dest_path, ContentFile(new_file.read()))
                new_file.close()

            for data_id in xrange(self.data_count):
                dest_path = dest_dir + str(data_id) + '.out'
                src_path = src_dir + str(data_id) + '.out'
                if default_storage.exists(dest_path):
                    default_storage.delete(dest_path)
                new_file = default_storage.open(src_path)
                default_storage.save(dest_path, ContentFile(new_file.read()))
                new_file.close()

            return True

        except Exception as e:
            raise e
       
    def updateProblem(self, uid, prob_priv, prob_title, prob_time,
            prob_memory, prob_codelength, prob_desc, is_spj,
            data_count, course_id, case_info):
        try:
            if (Problem.isLegalTitle(prob_title)):
                self.prob_title = prob_title
            else:
                raise Exception(Problem.TITLE_ERRMSG)
            if (Problem._isLegalDesc(prob_desc)):
                self.prob_desc = prob_desc
            else:
                raise Exception(Problem.DESC_ERRMSG)

            self.prob_priv = prob_priv
            self.prob_title = prob_title
            self.prob_time = prob_time
            self.prob_memory = prob_memory
            self.prob_codelength = prob_codelength
            self.is_spj = is_spj
           #self.author = User.getById(uid) #will change the author...
            self.data_count = data_count
            self.course = Course.getById(course_id)
            self.case_info = case_info

            self.save()
            return True
        except Exception as e:
            raise e

    @classmethod
    def addProblem(cls, uid, prob_priv, prob_title, prob_time, 
            prob_memory, prob_codelength, prob_desc, is_spj,
            data_count, course_id, case_info):
        try:
            p = Problem()
            if (cls.isLegalTitle(prob_title)):
                p.prob_title = prob_title
            else:
                raise Exception(cls.TITLE_ERRMSG)
            if (cls._isLegalDesc(prob_desc)):
                p.prob_desc = prob_desc
            else:
                raise Exception(cls.DESC_ERRMSG)

            p.prob_priv = prob_priv
            p.prob_title = prob_title
            p.prob_time = prob_time
            p.prob_memory = prob_memory
            p.prob_codelength = prob_codelength
            p.is_spj = is_spj
            p.author = User.getById(uid)
            p.data_count = data_count
            p.course = Course.getById(course_id)
            p.case_info = case_info

            p.save()
            return p
        except Exception as e:
            raise e

    def deleteProblem(self, uid):
        try:
            if (User.getById(uid) != self.author):
                raise Exception(cls.PRV_ERRMSG)

            self.prob_priv = 0
            self.author =User.getById(1) #modified

            self.save()
            return self.pid
        except Exception as e:
            raise e

    def deleteProblem(self):
        try:
            self.prob_priv = 0
            self.author = User.getById(1) #modified
            self.course = Course.getById(9) # a course to store the deleted problems

            self.save()
            return self.pid
        except Exception as e:
            raise e


    def canManageProblem(self, u):
        try:
            if self.author == u:
                return True
            if self.course.admin == u:
                return True
            if self.course.school.admin == u:
                return True
            if self.course.school.university.admin == u:
                return True
            return False
        except Exception as e:
            raise e

    def canViewProblem(self, u):
        try:
            if self.prob_priv == 'public':
                return True

            if self.prob_priv == 'protected' and u.priv != 'student':
                return True

            if self.canManageProblem(u):
                return True
            return False
        except Exception as e:
            raise e

    @classmethod
    def problemListByAuthor(cls, u):
        try:
            return Problem.objects.filter(
                    author=u).order_by('-pid')
        except Exception as e:
            raise e

    @classmethod
    def problemList(cls, u):
        try:
            ap = Problem.objects.filter(course__school__university=u.university).order_by('pid')
            res = []
            for p in ap:
                if p.canViewProblem(u):
                    res.append(p)
            return res
        except Exception as e:
            raise e

    @classmethod
    def problemManageList(cls, u):
        try:
            ap = Problem.objects.filter(course__school__university=u.university).order_by('-pid')
            res = []
            for p in ap:
                if p.canManageProblem(u):
                    res.append(p)
            return res
        except Exception as e:
            raise e

    @classmethod
    def canAddCourseProblem(cls, cs, u):
        if cs.canBeManaged(u):
            return True
        try:
            for css in CourseClass.getByCourse(cs):
                if css.canBeManaged(u):
                    return True
            return False
        except Exception as e:
            raise e
        
    def canViewInCourseClass(self, cc):
        try:
            if self.course == cc.course:
                return True
            return False
        except Exception as e:
            raise e

    def generateTestDataPreview(self, case_id, mode):
        try:
            problem_id = self.pid
            case_id = int(case_id)
            mode = int(mode)
            dir_path = Const.PROBLEM_DATA_PATH + str(problem_id) + '/'
            file_path = dir_path + str(case_id) + ('.in' if mode == 0 else '.out')
            if not default_storage.exists(file_path):
                raise Exception(u'数据文件不存在')

            new_file = default_storage.open(file_path)
            content = new_file.read(Const.PREVIEW_TESTDATA_MAXSIZE)
            if Const.PREVIEW_TESTDATA_MAXSIZE < os.stat(file_path).st_size:
                content += '(and more...)'
            new_file.close()

            return content

        except Exception as e:
            raise e

