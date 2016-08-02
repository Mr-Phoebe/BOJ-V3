from django.conf.urls import patterns, url
from Problem import views

urlpatterns = patterns('',
        url(r'^list/(\d+)/$', views.listProblem, name='list'),
        url(r'^list/$', views.listProblem, name='list'),
        url(r'^manage/$', views.listManageProblem, name='manage'),
        url(r'^manage/(?P<pageId>\d+)/$', views.listManageProblem, name='manage'),
        #url(r'^listManager/(\d+)/$', views.listManageProblem, name='listmanager'),
        #url(r'^listManager/$', views.listManageProblem, name='listmanager'),
        url(r'^p/(\d+)/$', views.showProblem, name='problem'),

        url(r'^contest/(?P<c_id>\d+)/problem/(?P<idx>[A-Z])/$',views.showContestProblem, name="contest_problem"), 

        url(r'^addProblem/$',views.chooseCourse, name='addproblem_choosecs'),
        url(r'^addProblem/(\d+)/$',views.addProblem, name='addproblem'),
        url(r'^addProblemSubmit',views.addProblemSubmit, name='addcommit'),
        url(r'^updateProblem/(\d+)/$', views.updateProblem, name='updateproblem'),
        url(r'^deleteProblem/(?P<problem_id>\d+)/$', views.deleteProblem, name='deleteproblem'),
        url(r'^updateProblemSubmit/(\d+)/$',views.updateProblemSubmit, name='updatecommit'),
        url(r'^getProblemTitle/$', views.getProblemTitle, name='title'),
        #        url(r'^addData/$', views.addData),
        #        url(r'^updateData/(\d+)/$', views.updateData),
        #url(r'^test/$',views.testPage),
        url(r'^addProblem/upload$',views.testUpload, name='upload'),
        url(r'^testUploadSubmit/$',views.testUploadSubmit, name='testups'),
        url(r'^testdata/(?P<problem_id>\d+)/(?P<case_id>\d+)/(?P<mode>\d+)/$', views.previewTestData, name = 'previewtestdata'),
        )
