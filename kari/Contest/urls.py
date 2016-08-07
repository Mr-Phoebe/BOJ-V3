from django.conf.urls import patterns, url
from Contest import views

urlpatterns = patterns('',
        url(r'^$', views.listContestByUser, name='list_available_contests'),
        url(r'^page/(?P<pageId>\d+)/$', views.listContestByUser, name='list_user_contest'),
        url(r'^manage/$', views.listContestByUserAndPriv, name='list_user_contest_manage'),
        url(r'^manage/page/(?P<pageId>\d+)/$', views.listContestByUserAndPriv, name='list_user_contest_manage'),
        url(r'^myself/$', views.listContestByAuthor, name='list_user_contest_myself'),
        url(r'^myself/page/(?P<pageId>\d+)/$', views.listContestByAuthor, name='list_user_contest_myself'),
        url(r'^courseclass/(?P<ccId>\d+)/$', views.listContest, name='list_contest'),
        url(r'^courseclass/(?P<ccId>\d+)/page/(?P<pageId>\d+)/$', views.listContest, name='list_contest'),
        url(r'^manage/courseclass/(?P<ccId>\d+)/$', views.listContestByPriv, name='list_contest_manage'),
        url(r'^manage/courseclass/(?P<ccId>\d+)/page/(?P<pageId>\d+)/$', views.listContestByPriv, name='list_contest_manage'),
        url(r'^(?P<cId>\d+)/$', views.showContest, name='show_contest'),
        url(r'^add/$', views.chooseCourseClass, name='add_contest_choose'), 
        url(r'^add/courseclass/(?P<ccId>\d+)/$', views.addContest, name='add_contest'), 
        url(r'^update/(?P<cId>\d+)/$', views.updateContest, name='update_contest'), 
        url(r'^release_board/(?P<cId>\d+)/$', views.releaseBoardTime, name='release_board'), 
        url(r'^notice/contest/(?P<cId>\d+)/$', views.listContestNotice, name='list_contest_notice'),
        url(r'^(?P<cId>\d+)/notice/(?P<cnId>\d+)/$', views.showContestNotice, name='show_contest_notice'), 
        url(r'^notice/add/contest/(?P<cId>\d+)/$', views.addContestNotice, name='add_contest_notice'), 
        url(r'^notice/update/(?P<cnId>\d+)/contest/(?P<cId>\d+)/$', views.updateContestNotice, name='update_contest_notice'), 
        url(r'^getContestNoticeList/$', views.getContestNoticeList, name='get_contest_notice_list'),

        url(r'^clarifications/(?P<cid>\d+)/$', views.viewAllClarifications, name='view_all_clars'),
        url(r'^clarifications/add/(?P<cid>\d+)/$', views.addClarification, name='add_clar'),
        url(r'^clarifications/answer/(?P<clar_id>\d+)/$', views.answerClarification, name='answer_clar'),
        url(r'^clarifications/delete/(?P<clar_id>\d+)/$', views.deleteClarification, name='delete_clar'),
        url(r'^all/$', views.listContestByUserAll, name='list_all_contests'),

        #url(r'^contestself$', views.listContestByUserSelf),
        )
