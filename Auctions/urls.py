from django.conf.urls.defaults import patterns, include

from Auctions import views


from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    (r'^$', views.index),

)