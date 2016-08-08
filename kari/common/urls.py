from django.conf.urls import patterns, include, url
from Cheat import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'kari.views.home', name='home'),
    # url(r'^kari/', include('kari.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	# url( r'^[Pp]roblem/', include( 'Problem.urls', namespace='Problem' )),
    #url(r'/goBack/$',views.goBack),
	url(r'^addrecord/(?P<cid>\d+)/$', views.addRecord, name='add_cheat_record'),
    url(r'^showresult/(?P<cid>\d+)/$', views.showResult, name='show_cheat_result'),
    url(r'^showresult/(?P<cid>\d+)/page/(?P<page>\d+)/$', views.showResult, name='show_cheat_result'),
    # url(r'^showresult/(?P<sid_a>\d+)/(?P<sid_b>\d+)/$', views.showCodeDiff, name='show_code_diff'),
    url(r'^codediff/(?P<ct_id>\d+)/$', views.showCodeDiff, name='show_code_diff'),
)
