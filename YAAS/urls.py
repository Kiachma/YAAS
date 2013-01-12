
from django.conf.urls import patterns, url, include

from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    url(r'^auctions/', include('Auctions.urls')),
    url(r'^admin/', include(admin.site.urls)),
)