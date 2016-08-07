from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from lyy import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kari.views.home', name='home'),
    # url(r'^kari/', include('kari.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url( r'^$', views.index, name='index'),
    url( r'^index/$', views.index, name='index'),
    url( r'^board/$', views.board, name='board'),
    url( r'^showStudent/$', views.showStudentByCCId, name='showStudent'),
    url( r'^showCourseClass/$', views.showCourseClass, name='showCourseClass'),
)
