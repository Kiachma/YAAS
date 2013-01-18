
from django.conf.urls import patterns, url, include
import views
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    url(r'^auctions/', include('Auctions.urls',namespace='auctions')),
    url(r'^users/', include('User.urls',namespace='user')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.base),
)