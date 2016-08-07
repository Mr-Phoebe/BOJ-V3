from django.conf.urls import patterns, url
from User import views

urlpatterns = patterns('',
    url(r'^$', views.showUserInfo, name='showinfo'),
    url(r'^update/$', views.update, name='update'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^add/student/$', views.addMultiUser, name='addstudent'),
    url(r'^add/admin/$', views.addAdmin, name='addadmin'),
    url(r'^add/school/$', views.addSchool, name='addschool'),
    url(r'^add/group/$', views.addGroup, name='addgroup'),
    url(r'^viewuser/(?P<uid>\d+)/$', views.viewUserInfo, name='viewuser'),
    url(r'^reset/(?P<uid>\d+)$', views.ResetPasswd, name='reset'),
    url(r'^school/(?P<school_id>\d+)/$', views.showSchool, name='show_school'),
    url(r'^school/(?P<school_id>\d+)/page/(?P<page_id>\d+)/$', views.showSchool, name='show_school'),
    url(r'^manage/admin/$', views.listAdmin, name='manageadmin'),
    url(r'^manage/student/$', views.listStudent, name='managestudent'),
    url(r'^manage/student2/$', views.listStudent2, name='managestudent'),
    url(r'^manage/student/page/(?P<page_id>\d+)/$', views.listStudent, name='managestudent'),
    url(r'^manage/student/page/(?P<page_id>\d+)/$', views.listStudent2, name='managestudent'),
    url(r'^manage/school/$', views.manageSchool, name='manageschool'),
    url(r'^manage/group/$', views.manageGroup, name='managegroup'),
    url(r'^manage/group/page/(?P<pageId>\d+)/$', views.manageGroup, name='managegroup'),
   
    url(r'^modify/school/(?P<school_id>\d+)$', views.modifySchool, name='modifyschool'),
    url(r'^modify/group/(?P<group_id>\d+)$', views.modifyGroup, name='modifygroup'),
    url(r'^modify/group/(?P<group_id>\d+)/resetall/$', views.resetGroupMemberPasswdHomepage, name='resetgrouphomepage'),
    url(r'^modify/group/(?P<group_id>\d+)/resetall/(?P<mode>[a-z]+)$', views.resetGroupMemberPasswd, name='resetgroup'),
    url(r'^modify/group/(?P<group_id>\d+)/delmember/(?P<user_id>\d+)$', views.delMember, name='delgroupmember'),
    url(r'^modify/group/(?P<group_id>\d+)/addmember/$', views.addMember, name='addgroupmember'),
    url(r'^download/(?P<usname>.+)/$',views.csvDownload,name='csvdownload'),
)

