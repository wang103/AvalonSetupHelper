from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),

  url(r'^(?P<room_id>[0-9]+)/$', views.room_info_before_join, name='room_info_before_join'),

  url(r'^(?P<room_id>[0-9]+)/player/(?<player_token>.+)/$', views.room_info_after_join, name='room_info_after_join'),

  url(r'^(?P<room_id>[0-9]+)/join_room/$', views.join_room, name='join_room'),


  url(r'^host/$', views.host, name='host'),

  url(r'^create_room/$', views.create_room, name='create_room'),
]

