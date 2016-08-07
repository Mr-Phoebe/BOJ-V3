from django.conf.urls import patterns, include, url
from Api import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^user/(?P<uid>\d+)/?$', views.userDetail ),
    url(r'^group/(?P<gid>\d+)/?$', views.groupDetail ),
    url(r'^login/?$', views.userLogin ),
    url(r'^contest/(?P<cid>\d+)/board/?$', views.boardDetail ),
)
