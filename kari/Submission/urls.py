from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from Submission import views, general_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kari.views.home', name='home'),
    # url(r'^kari/', include('kari.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url( r'^$', views.index, name='index'),
    url( r'^(?i)index/$', views.index, name='index'),
    # url( r'^(?i)all/(\d+)/$', views.submissionList, name='all'),
    # url( r'^(?i)all/$', views.submissionList, name='all'),
    # url( r'^(?i)status/$', views.submissionList, name='status'),
    url( r'^(?i)rejudge/in_contest/(?P<sid>\d+)/$', views.rejudgeSubmission, name='contest_rejudge'),
    url( r'^(?i)status/$', general_views.generalSubmissionList, name='status'),
    url( r'^(?i)status/page/(?P<page_id>\d+)/$', general_views.generalSubmissionList, name='status'),
    url( r'^(?i)submit/(?P<problem_id>\d+)/$', general_views.addGeneralSubmission, name='general_submit'),
    url( r'^(?i)submit/$', general_views.addGeneralSubmission, name='general_submit'),
    url( r'^(?i)detail/(?P<gsid>\d+)/$', general_views.viewCodeAndInfo, name='general_code_and_info'),
    url( r'^(?i)rejudge/(\d+)/$', general_views.rejudgeGeneralSubmission, name='general_rejudge'),

    url( r'^status/contest/(?P<contest_id>\d+)/$', views.submissionList, name='contest_status'), # modified
    url( r'^status/contest/(?P<contest_id>\d+)/page/(?P<page_id>\d+)/$', views.submissionList, name='contest_status'), # modified
    url( r'^(?i)submit/contest/(?P<contest_id>\d+)/problem/(?P<problem_index>([A-Z]))/$', views.addSubmission, name='submit'), # modified
    url( r'^(?i)detail/in_contest/(\d+)/$', views.viewCodeAndInfo, name='code_and_info'),
)
