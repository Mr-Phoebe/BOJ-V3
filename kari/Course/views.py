# Create your views here.
# coding: utf-8
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.core.urlresolvers import reverse

from django.core.paginator import Paginator

from User.models import *
from Problem.models import *
from Contest.models import *
from Course.models import *

from Course.forms import *

from kari.const import Const
from common.err import Err

import logging

logger = logging.getLogger('django')

def index(request):
    logger.info(str(request).replace("\n","\t"))
    return HttpResponse("Here is course page!")

def addCourse( request, school_id=None): # new
    logger.info(str(request).replace("\n","\t"))
    """
    views used to add Course
    """
    tpl = { 'sp': True }
    try:
        u = User.getSessionUser( request.session)
        if not u:
            raise Err( request, err='not login')

        if u.priv != 'university':
            raise Err( request, err='no priv')

        if not school_id:
            schools = School.objects.filter( university=u.university)
            return render( request, 'newtpl/course/add_course_select_school.html',  { 'school_list': schools, 'tpl': tpl }, )

        school_id = int( school_id)
        try:
            school = School.getById( school_id)
        except:
            raise Err( request, err='no school',
                    log_format=( '{0}'.format( school_id), ''),
                    user_format=( u'{0}'.format( school_id), u'搞错了啊亲！'),
                    )

        if not Course.canDoCourse( school.university, u):
            raise Err( request, err='no priv')

        # admin to be added or NULL
        user_list = User.objects.filter( university=school.university).filter( priv='course')
        form = modifyCourseForm( user_list, request.POST)
            
        if request.method == 'POST':
            if form.is_valid():
                if form.cleaned_data['admin']:
                    try:
                        admin = form.cleaned_data['admin']
                    except:
                        admin = None
                else:
                    admin = None
                no = form.cleaned_data['no']
                name = form.cleaned_data['name']
                try:
                    new_id = Course.addCourse( school, admin, no, name).id
                except Exception as e:
                    raise e
                    raise Err( request, 'example err',
                            log_format=( str(e), ''),
                            user_format=( unicode(e), ''),
                            )
                
                return redirect( 'Course:showCourse', course_id=new_id)
            else:
                raise Exception( u'表格有问题?')

        # not POST method
        else:
            form = modifyCourseForm( user_list)

        return render( request, 'newtpl/course/add_course.html',  { 'form': form, 'school': school, 'tpl': tpl }, )

    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render( request, Err.ERROR_PAGE, { 'errmsg': unicode(e), })

def updateCourse( request, course_id=None): # new
    logger.info(str(request).replace("\n","\t"))
    """
    views used to update Course
    """
    tpl = { 'sp': True, 'update': True }
    try:
        course_id = int( course_id)
        u = User.getSessionUser( request.session)

        if not u:
            raise Err( request, err='not login')
    
        try:
            course = Course.getById( course_id)
        except:
            raise Err( request, err='no course',
                    log_format=( '{0}'.format( course_id), ''),
                    user_format=( u'{0}'.format( course_id), u'别搞笑好嘛！！'),
                    )

        school = course.school
        if not Course.canDoCourse( school.university, u):
            raise Err( request, err='no priv')

        user_list = User.objects.filter( university=school.university).filter( priv='course')
        if request.method == 'POST':
            form = modifyCourseForm( user_list, request.POST)
            if form.is_valid():
                if form.cleaned_data['admin']:
                    try:
                        admin = form.cleaned_data['admin']
                    except:
                        admin = None
                else:
                    admin = None
                no = form.cleaned_data['no']
                name = form.cleaned_data['name']

                try:
                    Course.updateCourse( course_id, school, admin, no, name)
                except Exception as e:

                    if str(e).find('same') != -1:
                        u_e = u'具有相同编号和名称的课程已存在！'

                    raise Err( request, err='example err',
                            log_format=( str(e), ''),
                            user_format=( unicode(u_e) if u_e else unicode(e), u'搞死我了'),
                            )
                
                return redirect( 'Course:showCourse', course_id = course.id)
        # not POST method
        else:

            form = modifyCourseForm( 
                    user_list,
                    initial={
                        'admin': course.admin,# if course.admin else '',
                        'no': course.no,
                        'name': course.name,
                        }
                    )

        return render( request, 'newtpl/course/add_course.html',  { 'form': form, 'school': school, 'tpl':tpl, 'course': course}, )
    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render( request, Err.ERROR_PAGE, { 'errmsg': unicode(e), })

def deleteCourse( request, course_id=None): # new
    logger.info(str(request).replace("\n","\t"))
    """
    views used to delete Course
    """

    try:
        course_id = int(course_id)
        u = User.getSessionUser( request.session)
        if not u:
            raise Err( request, err = 'not login')

        try:
            course = Course.getById( course_id)
        except:
            raise Err( request, err='no course',
                    log_format=( '{0}'.format( course_id), ''),
                    user_format=( u'{0}'.format( course_id), u'别搞笑好嘛！！'),
                    )

        school = course.school

        if not Course.canDoCourse( school.university, u):
            raise Err( request, err = 'no priv')

        Course.deleteCourse( course_id)
    
        return redirect( 'User:show_school', school_id = school.id )

    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render( request, Err.ERROR_PAGE, { 'errmsg': str(e), }, )

def courseList( request, page_id='1'): # new
    logger.info(str(request).replace("\n","\t"))
    """
    views used to show Course List
    """

    tpl = { 'sp': True }
    try:
        page_id = int(page_id)
        u = User.getSessionUser( request.session)
        if not u:
            raise Err( request, err = 'not login')
    
        if u.priv == 'university':
            tpl['can_modify'] = True
        elif u.priv == 'school':
            tpl['can_manage'] = True
        elif u.priv != 'course':
            raise Err( request, err = 'no priv')
        
        courses = Course.getAllManagedCourses( u)

        return render( request, 'newtpl/course/course_list.html',  { 'course_list': courses, 'tpl': tpl}, )

    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render( request, Err.ERROR_PAGE, { 'errmsg': str(e), }, )

def showCourse( request, course_id=None): # new
    logger.info(str(request).replace("\n","\t"))
    """
    views used to show Course
    """

    tpl = { 'sp': True }
    try:
        course_id = int(course_id)
        u = User.getSessionUser( request.session)
        if not u:
            raise Err( request, err = 'not login')

        try:
            course = Course.getById( course_id)
        except:
            raise Err( request, err='no course',
                    log_format=( '{0}'.format( course_id), ''),
                    user_format=( u'{0}'.format( course_id), u'别搞笑好嘛！！'),
                    )

        if not course.canBeAccessed( u):
            raise Err( request, err = 'no priv')
        else:
            tpl['can_manage'] = True

        # total privilege( university )
        if Course.canDoCourse( course.school.university, u):
            tpl['can_modify'] = True
            
        # privilege to set admin( university & school)
        if course.canSetAdmin( u):
            tpl['can_set_admin'] = True

        tpl['page_selected'] = 'index'

        # course_classes = CourseClass.getByCourse( course)

        # problems = Problem.objects.filter( course_id=course.id)

        return render( request, 'newtpl/course/course.html',  { 'course': course, 'tpl': tpl}, )

    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render( request, Err.ERROR_PAGE, { 'errmsg': unicode(e)}, )

def showCourseProblems( request, course_id=None, page_id='1'): # new
    logger.info(str(request).replace("\n","\t"))
    """
    views used to show problems of some Course
    """

    tpl = { 'sp': True }
    try:
        course_id = int(course_id)
        page_id = int(page_id)
        u = User.getSessionUser( request.session)
        if not u:
            raise Err( request, err = 'not login')

        try:
            course = Course.getById( course_id)
        except:
            raise Err( request, err='no course',
                    log_format=( '{0}'.format( course_id), ''),
                    user_format=( u'{0}'.format( course_id), u'别搞笑好嘛！！'),
                    )

        if not course.canBeAccessed( u):
            raise Err( request, err = 'no priv')
        else:
            tpl['can_manage'] = True

        # total privilege( university )
        if Course.canDoCourse( course.school.university, u):
            tpl['can_modify'] = True
            
        # privilege to set admin( university & school)
        if course.canSetAdmin( u):
            tpl['can_set_admin'] = True

        tpl['page_selected'] = 'problem'

        problems = Problem.objects.filter( course_id=course.id)

        paginator = Paginator( problems, Const.PROBLEM_PER_PAGE)
        page_id = min(max(int(page_id), 1), paginator.num_pages)

        return render( request, 'newtpl/course/course_problem_list.html',  { 'course': course, 'problem_list': paginator.page( page_id), 'tpl': tpl}, )

    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render( request, Err.ERROR_PAGE, { 'errmsg': unicode(e)}, )

def showCourseClasses( request, course_id=None, page_id='1'): # new
    logger.info(str(request).replace("\n","\t"))
    """
    views used to show classes of some Course
    """

    tpl = { 'sp': True }
    try:
        course_id = int(course_id)
        page_id = int(page_id)
        u = User.getSessionUser( request.session)
        if not u:
            raise Err( request, err = 'not login')

        try:
            course = Course.getById( course_id)
        except:
            raise Err( request, err='no course',
                    log_format=( '{0}'.format( course_id), ''),
                    user_format=( u'{0}'.format( course_id), u'别搞笑好嘛！！'),
                    )

        if not course.canBeAccessed( u):
            raise Err( request, err = 'no priv')
        else:
            tpl['can_manage'] = True

        # total privilege( university )
        if Course.canDoCourse( course.school.university, u):
            tpl['can_modify'] = True
            
        # privilege to set admin( university & school)
        if course.canSetAdmin( u):
            tpl['can_set_admin'] = True

        tpl['page_selected'] = 'class'

        course_classes = CourseClass.getByCourse( course)

        paginator = Paginator( course_classes, Const.COURSE_PER_PAGE)
        page_id = min(max(int(page_id), 1), paginator.num_pages)

        return render( request, 'newtpl/course/course_classes.html',  { 'course': course, 'class_list': paginator.page(page_id), 'tpl': tpl}, )

    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render( request, Err.ERROR_PAGE, { 'errmsg': unicode(e)}, )

def setCourseAdmin( request, course_id=None):
    logger.info(str(request).replace("\n","\t"))
    """
    view used to set admin of some course
    """
    template_tags = {}
    u = None
    try:

        u = User.getSessionUser( request.session)
        if u == False:
            return render( request, 'error.html', { 'errmsg': Const.NOT_LOGGED_IN}, )

        course = Course.getById( course_id)

        if request.method == 'POST':
            new_admin = User.getById( request.POST['admin'])
            course.setAdmin( new_admin)
            
            return redirect( reverse( 'Course:showCourse', args=(course.id,)))
        else:
            users = User.listUserByPriv( 'course', course.school.university, course.school)

            return render( request, 'Course/SetAdmin.html',  { 'user': u, 'course': course, 'users': users, 'template_tags': template_tags, 'user': u }, )

    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render( request, 'error.html', { 'errmsg': unicode(e), 'user': u}, )

def addCourseClass( request, course_id=None):# new
    logger.info(str(request).replace("\n","\t"))
    """
    views used to add CourseClass
    """

    tpl = { 'sp': True }
    try:
        u = User.getSessionUser( request.session)
        if not u:
            raise Err( request, err='not login')
    
        if not course_id:
            schools = School.objects.filter( university=u.university)
            courses = Course.objects.filter( school__in=schools)
            return render( request, 'newtpl/course/add_class_select_course.html',  { 'course_list': courses, 'tpl': tpl }, )

        course_id = int(course_id)
        try:
            course = Course.getById( course_id)
        except:
            raise Err( request, err='no course',
                    log_format=( '{0}'.format( course_id), ''),
                    user_format=( u'{0}'.format( course_id), u'别搞笑好嘛！！'),
                    )

        if not course.canBeAccessed( u):
            raise Err( request, err = 'no priv')
            
        # user_list = [ ( u.username, u.username) for u in filter( lambda x: x.school == course.school and x.priv == 'courseclass', User.objects.all())]
        # user_list = [ ( usr.username, usr.username) for usr in filter( lambda x: x.school.university == course.school.university and ( x.school == course.school or not x.school) and x.priv == 'courseclass', User.objects.all())]
        user_list = User.objects.filter( university=course.school.university).filter( priv='courseclass')
        # user_list.insert(0, ('',u'无'))

        form = modifyCourseClassForm( user_list, request.POST)

        if request.method == 'POST':
            if form.is_valid():
                admin = form.cleaned_data['admin']

                name = form.cleaned_data['name']
                year = form.cleaned_data['year']

                try:
                    new_id = CourseClass.addCourseClass( course, admin, name, year)
                except Exception as e:
                    raise Err( request, err='example err',
                            log_format=( str(e), ''),
                            user_format=( unicode(e), u'出什么事情了？'),
                            )

                return redirect( 'Course:showCourseClass', course_class_id = new_id)
        # non post
        else:
            form = modifyCourseClassForm( user_list )


        return render( request, 'newtpl/course/add_course_class.html',  { 'form': form, 'user': u, 'course': course, 'tpl': tpl}, )

    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render( request, Err.ERROR_PAGE, { 'errmsg': unicode(e), }, )

def updateCourseClass( request, course_class_id=None):# new
    logger.info(str(request).replace("\n","\t"))
    """
    views used to update CourseClass
    """

    tpl = { 'sp': True }
    tpl['update'] = True
    try:
        course_class_id = int( course_class_id)
        u = User.getSessionUser( request.session)
        
        if not u:
            raise Err( request, err='not login')
    
        try:
            course_class = CourseClass.getById( course_class_id)
        except:
            raise Err( request, err='no courseclass', 
                    log_format=( '{0}'.format( course_class_id), ''), 
                    user_format=( u'{0}'.format( course_class_id), u'干什么呢这是！'),
                    )

        course = course_class.course
        if not CourseClass.canDoCourseClass( course, u):
            raise Err( request, err = 'no priv')

        user_list = User.objects.filter( university=course.school.university).filter( priv='courseclass')
        if request.method == 'POST':
            form = modifyCourseClassForm( user_list, request.POST)
            if form.is_valid():
                if form.cleaned_data['admin']:
                    admin = form.cleaned_data['admin']
                else:
                    admin = course_class.admin
                name = form.cleaned_data['name']
                year = form.cleaned_data['year']

                try:
                    CourseClass.updateCourseClass( course_class, course, admin, name, year)
                except Exception as e:
                    raise Err( request, err='example err',
                            log_format=( str(e), ''),
                            user_format=( unicode(e), u'出什么事情了？'),
                            )
                
                return redirect( 'Course:showCourseClass', course_class_id = course_class.id )
        # not POST method
        else:
            # user_list = [ ( usr.username, usr.username) for usr in filter( lambda x: x.school.university == course.school.university and ( x.school == course.school or not x.school) and x.priv == 'courseclass', User.objects.all())]

            form = modifyCourseClassForm( 
                    user_list,
                    initial={
                        'admin': course_class.admin,
                        'name': course_class.name,
                        'year': course_class.year,
                        }
                    )

        return render( request, 'newtpl/course/add_course_class.html',  { 'form': form, 'course': course, 'course_class': course_class, 'tpl': tpl}, )

    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render( request, Err.ERROR_PAGE, { 'errmsg': unicode(e), }, )

def deleteCourseClass( request, course_class_id=None): # new
    logger.info(str(request).replace("\n","\t"))
    """
    views used to delete CourseClass
    """

    try:
        course_class_id = int(course_class_id)
        u = User.getSessionUser( request.session)
        if not u:
            raise Err( request, err = 'not login')

        try:
            course_class = CourseClass.getById( course_class_id)
        except:
            raise Err( request, err='no courseclass', 
                    log_format=( '{0}'.format( course_class_id), ''), 
                    user_format=( u'{0}'.format( course_class_id), u'干什么呢这是！'),
                    )

        course = course_class.course
        if not CourseClass.canDoCourseClass( course, u):
            raise Err( request, err = 'no priv')

        CourseClass.deleteCourseClass( course_class_id)
    
        return redirect( 'Course:showCourse', course_id = course.id )

    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render( request, Err.ERROR_PAGE, { 'errmsg': unicode(e), }, )

def courseClassList( request, page_id='1'): # new
    logger.info(str(request).replace("\n","\t"))
    """
    views used to show CourseClass List
    """

    tpl = { 'sp': True}
    try:
        page_id = int(page_id)
        u = User.getSessionUser( request.session)
        if not u:
            raise Err( request, err = 'not login')
        
        if u.priv == 'student':
            course_classes = CourseClass.getByStudent( u)
        else:
            tpl['can_manage'] = True
            course_classes = CourseClass.getAllManagedClasses( u)

        if u.priv == 'university':
            tpl['can_modify'] = True
            tpl['can_set_admin'] = True

        if u.priv == 'school':
            tpl['can_set_admin'] = True

        paginator = Paginator( course_classes, Const.CLASS_PER_PAGE)
        page_id = min(max(int(page_id), 1), paginator.num_pages)

        return render( request, 'newtpl/course/course_class_list.html',  { 'course_class_list': paginator.page(page_id), 'tpl': tpl}, )

    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render( request, Err.ERROR_PAGE, { 'errmsg': unicode(e), }, )

def showCourseClass( request, course_class_id=None): # new
    logger.info(str(request).replace("\n","\t"))
    """
    views used to show CourseClass
    """

    tpl = {'sp':True}
    try:
        u = User.getSessionUser( request.session)
        if not u:
            raise Err( request, err = 'not login')

        try:
            course_class = CourseClass.getById( course_class_id)
        except:
            raise Err( request, err='no courseclass', 
                    log_format=( '{0}'.format( course_class_id), ''), 
                    user_format=( u'{0}'.format( course_class_id), u'干什么呢这是！'),
                    )

        if not course_class.canBeAccessed( u):
            raise Err( request, err = 'no priv')
        elif course_class.canBeManaged( u):
        # privilge to show all things( univ & shc & c & cc admin)
            tpl['can_manage'] = True
        else:
            tpl['can_show'] = True

        # total privilege( university & school)
        if CourseClass.canDoCourseClass( course_class.course, u):
            tpl['can_modify'] = True
            
        # privilege to set admin( university & school)
        if course_class.canSetAdmin( u):
            tpl['can_set_admin'] = True

        tpl['page_selected'] = 'index'

        return render( request, 'newtpl/course/course_class.html',  { 'course_class': course_class, 'tpl': tpl}, )

    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render( request, Err.ERROR_PAGE, { 'errmsg': unicode(e), }, )

def setCourseClassAdmin( request, course_class_id=None):
    logger.info(str(request).replace("\n","\t"))
    """
    view used to set admin of some course_class
    """
    template_tags = {}
    u = None
    try:
        u = User.getSessionUser( request.session)
        if u == False:
            return render( request, 'error.html', { 'errmsg': Const.NOT_LOGGED_IN}, )

        course_class = CourseClass.getById( course_class_id)

        if request.method == 'POST':
            new_admin = User.getById( request.POST['admin'])
            course_class.setAdmin( new_admin)
            
            return redirect( 'Course:showCourseClass', course_class_id = course_class.id )
        else:
            users = User.listUserByPriv( 'courseclass', course_class.course.school.university, course_class.course.school)

            return render( request, 'Course/SetAdmin.html',  { 'user': u, 'course_class': course_class, 'users': users, 'template_tags': template_tags, 'user': u }, )

    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render( request, 'error.html', { 'errmsg': unicode(e), 'user': u}, )

def addGroup( request, course_class_id=None, group_id=None): # new
    logger.info(str(request).replace("\n","\t"))
    """
    views used to add group to some courseclass
    """

    try:
        u = User.getSessionUser( request.session)
        if not u:
            raise Err( request, err = 'not login')

        try:
            course_class = CourseClass.getById( course_class_id)
        except:
            raise Err( request, err='no courseclass', 
                    log_format=( '{0}'.format( course_class_id), ''), 
                    user_format=( u'{0}'.format( course_class_id), u'干什么呢这是！'),
                    )
        
        if not CourseClass.canDoCourseClass( course_class.course, u):
            raise Err( request, err = 'no priv')

        if not group_id and request.method != 'POST':
            raise Err( request, err='request err', 
                    log_format=( '', ''), 
                    user_format=( '', ''), 
                    )
        # not post
        if group_id:
            group_id = int(group_id)

        if request.method == 'POST':

            if request.POST['group_add'] == '':
                return redirect( 'Course:groups', course_class_id = course_class.id )

            group_id = int( request.POST['group_add'])

        try:
            group = Group.getById( group_id)
        except:
            raise Err( request, err='no group', 
                    log_format=( '{0}'.format( group_id), ''), 
                    user_format=( u'{0}'.format( group_id), u'这！'),
                    )

        course_class.addGroup( group)

        return redirect( 'Course:groups', course_class_id = course_class.id )

    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render( request, Err.ERROR_PAGE, { 'errmsg': unicode(e), }, )

def showCourseClassGroups( request, course_class_id=None, page_id='1'): # new
    logger.info(str(request).replace("\n","\t"))
    """
    views used to show groups of some courseclass
    """

    tpl = {'sp':True}
    try:
        page_id = int(page_id)
        u = User.getSessionUser( request.session)
        if not u:
            raise Err( request, err = 'not login')

        try:
            course_class = CourseClass.getById( course_class_id)
        except:
            raise Err( request, err='no courseclass', 
                    log_format=( '{0}'.format( course_class_id), ''), 
                    user_format=( u'{0}'.format( course_class_id), u'干什么呢这是！'),
                    )

        if not course_class.canBeAccessed( u):
            raise Err( request, err = 'no priv')
        elif course_class.canBeManaged( u):
        # privilge to show all things( univ & shc & c & cc admin)
            tpl['can_manage'] = True
        else:
            tpl['can_show'] = True

        if CourseClass.canDoCourseClass( course_class.course, u):
            tpl['can_modify'] = True

        groups = course_class.groups.all()
        school_groups = Group.objects.filter( school=course_class.course.school)
        groups_not_in_class = set(school_groups) - set( groups)

        groups_not_in_class = [ ( g.name, g.id) for g in groups_not_in_class]

        groups_not_in_class.insert( 0, ( '无', ''))
        paginator = Paginator( groups, Const.GROUP_PER_PAGE)
        page_id = min(max(int(page_id), 1), paginator.num_pages)

        tpl['page_selected'] = 'group'

        return render( request, 'newtpl/course/course_class_group_list.html',  { 'course_class': course_class, 'group_list': paginator.page(page_id), 'groups_waiting': groups_not_in_class, 'tpl': tpl}, )

    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render( request, Err.ERROR_PAGE, { 'errmsg': unicode(e), }, )

def showCourseClassContests( request, course_class_id=None, page_id='1'):# new
    logger.info(str(request).replace("\n","\t"))
    """
    views used to show contests of some courseclass
    """

    tpl = {'sp':True}
    try:
        page_id = int(page_id)
        u = User.getSessionUser( request.session)
        if not u:
            raise Err( request, err = 'not login')

        try:
            course_class = CourseClass.getById( course_class_id)
        except:
            raise Err( request, err='no courseclass', 
                    log_format=( '{0}'.format( course_class_id), ''), 
                    user_format=( u'{0}'.format( course_class_id), u'干什么呢这是！'),
                    )

        if not course_class.canBeAccessed( u):
            raise Err( request, err = 'no priv')
        elif course_class.canBeManaged( u):
        # privilge to show all things( univ & shc & c & cc admin)
            tpl['can_manage'] = True
        else:
            tpl['can_show'] = True

        if CourseClass.canDoCourseClass( course_class.course, u):
            tpl['can_modify'] = True

        contests = Contest.getByCourseClass(course_class)
        now = datetime.now()
        for c in contests:
            c.course_class_name = unicode(c.course_class.getFullName())
            c.title = unicode(c.contest_title)
            if c.start_time+timedelta(minutes=c.length)<now:
                c.status = 'ended'
            elif c.start_time > now:
                c.status = 'scheduled'
            else:
                c.status = 'running'

        paginator = Paginator(contests, Const.CONTEST_PER_PAGE)
        page_id = min(max(int(page_id), 1), paginator.num_pages)

        tpl['page_selected'] = 'contest'

        return render( request, 'newtpl/course/course_class_contest_list.html',  { 'course_class': course_class, 'contest_list': paginator.page(page_id),  'tpl': tpl}, )

    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render( request, Err.ERROR_PAGE, { 'errmsg': unicode(e), }, )

def showCourseClassStudents( request, course_class_id=None, page_id='1'): # new
    logger.info(str(request).replace("\n","\t"))
    """
    views used to show all students of some courseclass
    """

    tpl = {'sp':True}
    try:
        page_id = int(page_id)
        u = User.getSessionUser( request.session)
        if not u:
            raise Err( request, err = 'not login')

        try:
            course_class = CourseClass.getById( course_class_id)
        except:
            raise Err( request, err='no courseclass', 
                    log_format=( '{0}'.format( course_class_id), ''), 
                    user_format=( u'{0}'.format( course_class_id), u'干什么呢这是！'),
                    )

        if not course_class.canBeAccessed( u):
            raise Err( request, err = 'no priv')
        elif course_class.canBeManaged( u):
        # privilge to show all things( univ & shc & c & cc admin)
            tpl['can_manage'] = True
        else:
            tpl['can_show'] = True

        if CourseClass.canDoCourseClass( course_class.course, u):
            tpl['can_modify'] = True

        students = course_class.getAllStudents()

        for s in students:
            s.groups = []
            for g in course_class.groups.all():
                if s.belongsToGroup( g):
                    s.groups.append( g)

        tpl['page_selected'] = 'student'

        paginator = Paginator( students, Const.STUDENT_PER_PAGE)
        page_id = min(max(int(page_id), 1), paginator.num_pages)

        return render( request, 'newtpl/course/course_class_student_list.html',  { 'user': u, 'course_class': course_class, 'student_list': paginator.page(page_id), 'tpl': tpl}, )

    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render( request, Err.ERROR_PAGE, { 'errmsg': unicode(e), }, )

def showCourseClassProblems( request, course_class_id=None, page_id = '1'): # new
    logger.info(str(request).replace("\n","\t"))
    """
    views used to show problems that some courseclass can touch
    """

    tpl = {'sp':True}
    try:
        page_id = int(page_id)
        u = User.getSessionUser( request.session)
        if not u:
            raise Err( request, err = 'not login')

        try:
            course_class = CourseClass.getById( course_class_id)
        except:
            raise Err( request, err='no courseclass', 
                    log_format=( '{0}'.format( course_class_id), ''), 
                    user_format=( u'{0}'.format( course_class_id), u'干什么呢这是！'),
                    )

        if not course_class.canBeAccessed( u):
            raise Err( request, err = 'no priv')
        elif course_class.canBeManaged( u):
        # privilge to show all things( univ & shc & c & cc admin)
            tpl['can_manage'] = True
        else:
            tpl['can_show'] = True

        if CourseClass.canDoCourseClass( course_class.course, u):
            tpl['can_modify'] = True

        problems = Problem.objects.filter( course_id=course_class.course.id)

        tpl['page_selected'] = 'problem'

        paginator = Paginator( problems, Const.PROBLEM_PER_PAGE)
        page_id = min(max(int(page_id), 1), paginator.num_pages)

        return render( request, 'newtpl/course/course_class_problem_list.html',  { 'course_class': course_class, 'problem_list': paginator.page(page_id), 'tpl': tpl}, )

    except Exception as e:
        logger.error(str(e).replace("\n","\t"))
        return render( request, Err.ERROR_PAGE, { 'errmsg': unicode(e), }, )
