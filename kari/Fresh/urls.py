from django.conf.urls import patterns, include, url
from Register import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.mainPage, name='home'),
    #url(r'^$', views.endedPage, name='home'),
    url(r'^team/$', views.teamRegister, name='team_register'),
    url(r'^team/reset/(?P<tid>\d+)/$', views.resetPasswd, name='reset_passwd'),
    url(r'^login/$', views.teamLogin, name='team_login'),
    url(r'^logout/$', views.teamLogout, name='team_logout'),
    url(r'^info/(?P<tid>\d+)/$', views.teamInfo, name='team_info'),
    url(r'^add_member/(?P<tid>\d+)/$', views.addTeamMember, name='add_member'),
    url(r'^modify_member/(?P<cid>\d+)/$', views.modifyTeamMember, name='modify_member'),
    
    url(r'^view_all_teams/$', views.viewAllTeams, name='view_teams'),
    url(r'^view_accepted_teams/$', views.viewAcceptedTeams, name='view_accepted_teams'),
    url(r'^admin_login/$', views.adminLogin, name='admin_login'),
    url(r'^admin_logout/$', views.adminLogout, name='admin_logout'),
    url(r'^judge_team/$', views.judgeTeam, name='judge_team'),
    url(r'^judge_team/(?P<tid>\d+)/$', views.judgeTeam, name='judge_team'),
    url(r'^judge_team_result/(?P<tid>\d+)/(?P<result>\w+)/$', views.judgeTeamResult, name='judge_team_result'),

 
    #url(r'^apply2/(?P<cid>\d+)/$', views.applyForContest2, name='apply2'),
    # url(r'^list/$', views.viewAllContestant, name='list'),
    # url(r'^kari/', include('kari.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	# url( r'^[Pp]roblem/', include( 'Problem.urls', namespace='Problem' )),
    #url(r'/goBack/$',views.goBack),
)
