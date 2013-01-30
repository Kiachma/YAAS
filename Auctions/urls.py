from django.conf.urls.defaults import patterns, include
from django.conf.urls import patterns, url

from Auctions import views


from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    url(r'^(?P<auction_id>|None|\d+)/edit$', views.edit , name='edit'),
    url(r'^(?P<auction_id>\d+)/$', views.view , name='view'),
    url(r'^(?P<auction_id>|None|\d+)/delete$', views.delete , name='delete'),
    url(r'^(?P<auction_id>|None|\d+)/save/$', views.save , name='save'),
    url(r'^(?P<auction_id>|None|\d+)/bid/$', views.bid , name='bid'),
    url(r'^confirm/', views.confirm ,name="confirm"),

)