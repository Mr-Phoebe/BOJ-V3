from django.conf.urls import patterns, include, url
from django.conf import settings
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

    #common url
    url( r'^$', 'common.views.index', name='index'),
    url( r'^login/$', 'common.views.login', name='login'),
    url( r'^logout/$', 'common.views.logout', name='logout'),
    url( r'^test/$', 'common.views.test', name='test'),
    url( r'^faq/$', 'common.views.faq', name='faq'),
    url( r'^whitepaper/$', 'common.views.whitepaper', name='whitepaper'),
    url( r'^abouttemp/$', 'common.views.about', name='about'),
    url( r'^register/$', 'common.views.register', name='register'),

    url( r'^contest/', include( 'Contest.urls', namespace='Contest')),
    url( r'^submission/', include( 'Submission.urls', namespace='Submission')),
    #url( r'^submission2/', include( 'Submission2.urls', namespace='Submission2')),
    url( r'^course/', include( 'Course.urls', namespace='Course')),
    url( r'^user/', include( 'User.urls', namespace='User')),
    url( r'^problem/', include( 'Problem.urls', namespace='Problem' )),
    url( r'^statistic/', include( 'Statistic.urls', namespace='Statistic' )),
    #url( r'^statistic2/', include( 'Statistic2.urls', namespace='Statistic2' )),
    url( r'^cheat/', include( 'Cheat.urls', namespace='Cheat' )),

    #url( r'^fresh/', include( 'Fresh.urls', namespace = 'Fresh')),    
    url( r'^apply/', include( 'Register.urls', namespace = 'Register')),    
    url( r'^ckeditor/', include('ckeditor.urls')),

    url( r'^print/', include('Print.urls')),

    url( r'^api/', include('Api.urls')),
)
"""
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/',include(debug_toolbar.urls)),
    )
"""
