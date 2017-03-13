from django.conf.urls import url
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login_view),
    url(r'^logout$', views.logout_view),
    url(r'^(?P<campus_id>[0-9]+)/$', views.show_calendar),
    url(r'^(?P<campus_id>[0-9]+)/create_event/$', views.create_event),
]