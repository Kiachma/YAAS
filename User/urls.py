from django.conf.urls.defaults import patterns, include
from django.conf.urls import patterns, url

from User import views


from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    url(r'^(?P<user_id>None|\d+)/$', views.index, name='index'),
    url(r'^(?P<user_id>None|\d+)/save/$', views.save , name='save'),
    url(r'^login/$', views.auth_login, name='login'),
    url(r'^logout/$', views.auth_logout, name='logout'),

)