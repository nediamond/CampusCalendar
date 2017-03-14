from django.contrib import admin
from django.contrib.auth.models import Group

from models import *

admin.site.unregister(Group)

@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(CampusCalendar)
class CCalendarAdmin(admin.ModelAdmin):
    list_display = ('id', 'campus', 'name')

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'campus', 'name')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'calendar')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'main_campus')
