from django.conf.urls import patterns, url
from Statistic import views

urlpatterns = patterns('',
        url(r'^board/(\d+)/$', views.showBoardByStatus, name='boardByAC'),
        url(r'^balloon/(\d+)/$', views.showBalloon, name='balloon'),
        url(r'^score/(\d+)/$', views.showBoardByDynamicScore, name='boardByDynamicScore'),
        url(r'^c/(?P<cid>\d+)/index/(?P<p_index>([A-Z]))/$', views.showContestProblemStatistics, name='contest_problem_st'),
        url(r'^p/(?P<pid>\d+)/$', views.showProblemStatistics, name='problem_st'),
        )
