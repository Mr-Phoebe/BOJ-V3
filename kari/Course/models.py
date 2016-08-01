# coding: utf
from django.db import models
from kari.const import Const
from kari.conf import flush_transaction
from User.models import User, School, Group

from django.core.exceptions import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS

class Course(models.Model):
    """
    Course Model
    """

    # foreign key
    school = models.ForeignKey( 'User.School', verbose_name='the school belonged to')
    admin = models.ForeignKey( 'User.User', blank=True, null=True, verbose_name='admin of the course')

    # attributes
    no = models.CharField( max_length=20, verbose_name='the notable name used by school')
    name = models.CharField( max_length=100, verbose_name='the name of the course')

    # meta options
    class Meta:
        unique_together = ( ( 'school', 'no'), )

    def __unicode__(self):
        return self.name

    # function

    @classmethod
    def getById( cls, course_id):
        """
        get Course by ID, and validate the param ID
        """
        try:
            course = cls.objects.get(pk=course_id)
        except:
            raise Exception( Const.COURSE_NOT_EXIST.format(course_id))

        return course 

    @classmethod
    def canDoCourse( cls, university, user):
        """
        whether a user can add a course or not
        admin of school cannot do such things
        """
        #if self.school.admin == user:
        #    return True
        #if self.school.university.admin == user:
        #    return True
        #return False

        if university.isAdmin( user):
            return True
        # we can not raise Exception everywhere
        return False

    @classmethod
    def canListCourse( cls, school, user):
        """
        whether a user can list courses of some school or not
        """
        if cls.canDoCourse( school.university, user):
            return True
        if school.isAdmin( user):
            return True

        return False

    def canBeAccessed( self, user):
        """
        whether a user can touch the very course or not
        """
        if Course.canDoCourse( self.school.university, user):
            return True
        # school admin
        if self.school.isAdmin( user):
            return True
        # course admin 
        if self.isAdmin( user):
            return True

        return False

    def getFullName(self):
        return ' - '.join([self.no, self.name])

    @classmethod
    def addCourse( cls, school, admin, notable, course_name):
        """
        to add Course
        """
        course = Course()
        course.school = school
        if admin:
            course.admin = admin
        course.no = notable
        course.name = course_name
        # unique_together validation
        try:
            course.validate_unique()
        except:
            raise Exception( Const.UNIQUE_TOGETHER_VALIDATION_FAILED)
        course.save()

        return course

    @classmethod
    def updateCourse( cls, crs_id=None, school=None, admin=None, notable=None, course_name=None):
        """
        to update Course
        """
        try:
            course = cls.getById( crs_id)
        except:
            raise

        course.school = school
        if admin:
            course.admin = admin
        course.no = notable
        course.name = course_name

        try:
            course.validate_unique()
        except:
            raise 
            # raise Exception( Const.UNIQUE_TOGETHER_VALIDATION_FAILED)

        course.save()

        return True

    @classmethod
    def deleteCourse( cls, crs_id):
        """
        to delete Course
        """
        try:
            course = cls.getById( crs_id)
        except:
            raise

        course.delete()
        return True

    def canBeManaged( self, user):
        """
        whether a course can be managed by the very user
        managing means adding contest and adding problems
        """
        if Course.canDoCourse( self.school.university, user):
            return True
        # no admin of other courses could modify
        # ever bugged
        if self.isAdmin( user):
            return True
        return False


    def isAdmin( self, user):
        """
        user is the admin of the course or not
        """
        if user.priv == 'course' and user == self.admin:
            return True
        return False

    def canSetAdmin( self, user):
        """
        can some super admin change the admin of some course
        """
        if Course.canDoCourse( self.school.university, user):
            return True
        if self.school.isAdmin( user):
            return True

        return False

    def setAdmin( self, user):
        """
        set the user as the admin of the course, used by super admin
        """
        self.admin = user
        self.save()
        return True

    @classmethod
    def getByAdmin( cls, user):
        """
        return all courses managed by the very admin
        """
        courses = cls.objects.all()
        courses = courses.filter( admin=user).order_by('-id')
        return courses

    @classmethod
    def getBySchool( cls, the_school):
        """
        return all courses the school set up
        """
        courses = cls.objects.filter( school=the_school).order_by('-id')
        return courses

    @classmethod
    def getBySchoolAndNo( cls, the_school, the_no):
        """
        return all courses indexed by school and no
        """
        # the best method?
        courses = cls.objects.filter( school=the_school).filter( the_no).order_by('-id')
        return courses

    @classmethod
    def getAllManagedCourses( cls, user):
        """
        get all courses which can be managed by the very user
        """
        if user.priv != 'courseclass' and user.priv != 'student':
            courses = cls.objects.all()
            return filter( lambda x: x.canBeAccessed( user), courses)
        elif user.priv == 'courseclass':
            course_classes = CourseClass.objects.all()
            return list(set([ x.course for x in course_classes]))
        else:
            return None

    def validate_unique(self, *args, **kwargs):
        """
        override the validate_unique func
        """
        
        try:

            super( Course, self).validate_unique(*args, **kwargs)

        except:

            raise Exception( 'Course with same NO and NAME already exists.')

class CourseClass( models.Model):
    """
    Classes of the Course Model
    """

    # Constant

    # foreign key
    course = models.ForeignKey( 'Course', verbose_name='the course belonged to')
    admin = models.ForeignKey( 'User.User', verbose_name='admin of the class' )

    # many to many field
    groups = models.ManyToManyField( 'User.Group', blank=True, null=True, verbose_name='the group detail of the class')

    # attributes
    name = models.CharField( max_length=100, verbose_name='the name of the class')
    year = models.IntegerField( db_index=True, verbose_name='the year of the class')

    def __unicode__(self):
        return self.name

    def getFullName(self):
        return ' - '.join([str(self.year), self.course.name, self.name])

    # function

    @classmethod
    def getById( cls, cc_id):
        """
        get CourseClass by ID, and validate the param ID
        """
        try:
            course_class = cls.objects.get(pk=cc_id)
        except:
            raise Exception( Const.COURSECLASS_NOT_EXIST.format(cc_id))
        return course_class

    @classmethod
    def canDoCourseClass( cls, course, user):
        """
        whether a user can handle course_classes of some course or not
        """
        # no admin of other schools could modify
        if course.school.isAdmin( user):
            return True
        # no admin of other univs could modify
        if course.school.university.isAdmin( user):
            return True

        return False

    def canBeManaged( self, user):
        """
        whether a course class can be managed by the very user
        managing means adding contest and adding problems
        """
        if CourseClass.canDoCourseClass( self.course, user):
            return True
        # no admin of other courses could modify
        # ever bugged
        if self.course.isAdmin( user):
            return True
        if self.isAdmin( user):
            return True
        return False

    def canBeAccessed( self, user):
        """
        whether a user can touch the very course_class or not
        """
        if self.canBeManaged( user):
            return True
        # student
        if self.partOfGroups( user):
            return True

        return False

    @classmethod
    def addCourseClass( cls, course, admin, name, year):
        """
        to add CourseClass
        """
        course_class = CourseClass()
        course_class.course = course 
        course_class.admin = admin
        course_class.name = name
        course_class.year = year
        course_class.save()

        flush_transaction()

        return course_class.id

    @classmethod
    def updateCourseClass( cls, course_class, course=None, admin=None, name=None, year=None):
        """
        to update CourseClass
        """

        if course:
            course_class.course= course 
        if admin:
            course_class.admin = admin
        if name:
            course_class.name = name
        if year:
            course_class.year = year

        course_class.save()

        return True

    @classmethod
    def deleteCourseClass( cls, cc_id):
        """
        to delete CourseClass
        """
        try:
            course_class = cls.getById( cc_id)
        except:
            raise Exception( Const.COURSECLASS_NOT_EXIST.format( cc_id))
        course_class.delete()
        return True

    def addGroup( self, group):
        """
        add group to CourseClass, which is many_to_many field
        """
        self.groups.add( group)
        return True
    def isAdmin( self, user):
        """
        user is the admin of the course_class or not
        """
        #if user.priv == 'university':
        #    return True
        
        if user.priv == 'course' and user == self.course.admin:
            return True
        if user.priv == 'courseclass' and user == self.admin:
            return True

        return False

    def canSetAdmin( self, user):
        """
        can someone set the admin of the very course_class or not
        """
        if self.course.canSetAdmin( user):
            return True
        return False

    def setAdmin( self, user):
        """
        set the user as admin of the course_class
        """
        self.admin = user
        self.save()
        return True

    def partOfGroups( self, user):
        """
        user belongs to the groups of course_class or not
        """
        for i in self.groups.all():
            if user.belongsToGroup( i):
                return True
        
        return False
        # raise Exception( Const.USER_NOT_GROUP_MEMBER.format( user.username))

    def getAllStudents( self):
        """
        return all students of the very course_class
        """
        students = []
        for i in self.groups.all():
            students.extend(i.allMembers())

        students = list(set(students))
        # sort by uid
        students.sort(key=lambda x:x.uid, reverse=True)
        return students

    @classmethod
    def getByAdmin( cls, user):
        """
        return all course_classes managed by the very admin
        """
        course_classes = cls.objects.all().filter( admin=user).order_by('-id')
        return course_classes

    @classmethod
    def getByCourse( cls, the_course):
        """
        return all course_classes belonged to very course
        """
        course_classes = cls.objects.all().filter( course=the_course).order_by('-id')
        return course_classes

    @classmethod
    def getByStudent( cls, user):
        """
        return all course_classes the very student belonged to
        """
        course_classes = cls.objects.all()
        course_classes = [ i for i in course_classes for j in i.groups.all() if user.belongsToGroup( j)]
        return course_classes

    @classmethod
    def getAllManagedClasses( cls, user):
        """
        get all course classes which can be managed by the very user
        """
        course_classes = cls.objects.all()
        return filter( lambda c_c: c_c.canBeManaged( user), course_classes)
