
from django.conf.urls import patterns, url, include
import views
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    url(r'^auctions/', include('Auctions.urls',namespace='auctions')),
    url(r'^users/', include('User.urls',namespace='user')),
    url(r'^API/', include('API.urls',namespace='API')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<category_id>$)', views.base ,name="index"),
    url(r'^(?P<category_id>None)/', views.base ,name="index"),
    url(r'^(?P<category_id>\d+)/', views.base ,name="index"),
    url(r'^search/', views.search ,name="search"),
    url(r'^populateDb/', views.populateDb ,name="populateDb"),
    url(r'^changeLanguage/', views.changeLanguage ,name="changeLanguage"),
)