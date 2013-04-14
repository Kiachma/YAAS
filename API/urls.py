from django.conf.urls import patterns
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin

from API import views


admin.autodiscover()
urlpatterns = patterns('',
                       (r'^search/$|search/(.+)/$', views.apisearch),
                       # (r'^bid/(?P<auction_id>\d+)/(?P<amount>\d+)$', views.bid),


                       (r'^(?P<username>\w+)/auction/(?P<auction_id>\d+)/bid/(?P<amount>\d+)$', csrf_exempt(views.AuctionBid())),
)