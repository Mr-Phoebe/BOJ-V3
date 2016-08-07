from django.conf.urls import patterns, include, url
from Print import views

urlpatterns = patterns('',
    url( r'^$', views.submit, name='submit'),
)
