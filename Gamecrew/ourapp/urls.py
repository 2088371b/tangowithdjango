from django.conf.urls import patterns, url
from ourapp import views

urlpatterns = patterns('',
        url(r'^$', views.mainpage, name='mainpage'),
		url(r'^gamesearch', views.gamesearch, name='gamesearch'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/(?P<gameID_slug>[\w\-]+)/$', views.game, name='game'),)