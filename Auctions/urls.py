from django.conf.urls.defaults import patterns, include
from django.conf.urls import patterns, url

from Auctions import views


from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<auction_id>\d+)/$', views.detail , name='detail'),

)