from django.conf.urls import url
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login_post_view),
    url(r'^login/$', views.login_page),
    url(r'^logout/$', views.logout_view),
    url(r'^(?P<campus_id>[0-9]+)/$', views.show_calendar),
    # url(r'^campus_list/$', views.campus_list),
    url(r'^event_manager/$', views.event_manager),
    url(r'^delete_event/(?P<event_id>[0-9]+)/', views.delete_event),
    url(r'^create_event$', views.create_event),
    url(r'^create_event/$', views.create_event),
    url(r'^edit_event/(?P<event_id>[0-9]+)$', views.edit_event),
    url(r'^edit_event/(?P<event_id>[0-9]+)/$', views.edit_event),
]