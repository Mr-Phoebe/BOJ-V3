from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from Course import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kari.views.home', name='home'),
    # url(r'^kari/', include('kari.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    #url( r'^$', views.index, name='index'),
    #url( r'^index/$', views.index, name='index'),
    url( r'^(?P<course_id>\d+)/$', views.showCourse, name='showCourse'),
    url( r'^add/$', views.addCourse, name='addCourse'),
    url( r'^add/school/(?P<school_id>\d+)/$', views.addCourse, name='addCourse'),
    url( r'^update/(?P<course_id>\d+)/$', views.updateCourse, name='updateCourse'),
    # url( r'^delete/(?P<course_id>\d+)/$', views.deleteCourse, name='deleteCourse'),
    url( r'^setadmin/c/(?P<course_id>\d+)/$', views.setCourseAdmin, name='setCourseAdmin'),

    url( r'^list/school/(?P<school_id>\d+)/$', views.courseList, name='listCourse'),

    url( r'^courses/$', views.courseList, name='courses'),
    url( r'^courses/page/(?P<page_id>\d+)/$', views.courseList, name='courses'),
    url( r'^(?P<course_id>\d+)/problems/$', views.showCourseProblems, name='courseProblems'),
    url( r'^(?P<course_id>\d+)/problems/page/(?P<page_id>\d+)/$', views.showCourseProblems, name='courseProblems'),
    url( r'^(?P<course_id>\d+)/classes/$', views.showCourseClasses, name='courseClasses'),
    url( r'^(?P<course_id>\d+)/classes/page/(?P<page_id>\d+)/$', views.showCourseClasses, name='courseClasses'),

    url( r'^class/(?P<course_class_id>\d+)/$', views.showCourseClass, name='showCourseClass'),
    url( r'^class/add/$', views.addCourseClass, name='addCourseClass'),
    url( r'^class/add/course/(?P<course_id>\d+)/$', views.addCourseClass, name='addCourseClass'),
    url( r'^class/update/(?P<course_class_id>\d+)/$', views.updateCourseClass, name='updateCourseClass'),
    # url( r'^class/delete/(?P<course_class_id>\d+)/$', views.deleteCourseClass, name='deleteCourseClass'),
    url( r'^setadmin/cc/(?P<course_class_id>\d+)/$', views.setCourseClassAdmin, name='setCourseClassAdmin'),
    # url( r'^classes/course/(?P<course_id>\d+)/$', views.courseClassList, name='listCourseClass'),

    url( r'^classes/$', views.courseClassList, name='classes'),
    url( r'^classes/page/(?P<page_id>\d+)/$', views.courseClassList, name='classes'),
    url( r'^class/(?P<course_class_id>\d+)/groups/add/(?P<group_id>\d+)/$', views.addGroup, name='addGroup'),
    url( r'^class/(?P<course_class_id>\d+)/groups/add/$', views.addGroup, name='addGroup'),
    url( r'^class/(?P<course_class_id>\d+)/groups/$', views.showCourseClassGroups, name='groups'),
    url( r'^class/(?P<course_class_id>\d+)/contests/$', views.showCourseClassContests, name='showCourseClassContests'),
    url( r'^class/(?P<course_class_id>\d+)/students/$', views.showCourseClassStudents, name='students'),
    url( r'^class/(?P<course_class_id>\d+)/problems/$', views.showCourseClassProblems, name='showCourseClassProblems'),

    url( r'^class/(?P<course_class_id>\d+)/groups/page/(?P<page_id>\d+)/$', views.showCourseClassGroups, name='groups'),
    url( r'^class/(?P<course_class_id>\d+)/contests/page/(?P<page_id>\d+)/$', views.showCourseClassContests, name='showCourseClassContests'),
    url( r'^class/(?P<course_class_id>\d+)/students/page/(?P<page_id>\d+)/$', views.showCourseClassStudents, name='students'),
    url( r'^class/(?P<course_class_id>\d+)/problems/page/(?P<page_id>\d+)/$', views.showCourseClassProblems, name='showCourseClassProblems'),
)
