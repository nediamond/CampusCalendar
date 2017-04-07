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
    url(r'^campus_list/$', views.campus_list),
    url(r'^my_orgs/$', views.user_orgs),
    url(r'^(?P<org_id>[0-9]+)/create_event/$', views.create_event),
    url(r'^(?P<org_id>[0-9]+)/submit_event$', views.submit_event),
]