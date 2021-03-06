from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime as dt


class Campus(models.Model):
    name = models.TextField(max_length=60, unique=True, null=False, blank=False)

    def __unicode__(self):
        return self.name


class CampusCalendar(models.Model):
    name = models.TextField(max_length=120, null=False, blank=False)
    campus = models.ForeignKey(Campus, unique=False)

    class Meta:
        unique_together = (('name', 'campus',),)

    def __unicode__(self):
        return self.name


class Organization(models.Model):
    name = models.TextField(max_length=120, null=False, blank=False)
    campus = models.ForeignKey(Campus, unique=False)
    administrators = models.ManyToManyField(User)

    class Meta:
        unique_together = (('name', 'campus',),)

    def __unicode__(self):
        return self.name


class Event(models.Model):
    name = models.TextField(max_length=120, null=False, blank=False)
    datetime = models.DateTimeField(null=False, blank=False)
    endtime = models.TimeField(null=False, blank=False, default=dt.time(23, 59))
    location = models.TextField(max_length=250, null=False, blank=False) # Maybe a location-type specific field instead of text
    calendar = models.ForeignKey(CampusCalendar, unique=False)
    organization = models.ForeignKey(Organization, unique=False)
    description = models.TextField(max_length=500, null=True, blank=True)
    graphic = models.ImageField(upload_to='events/', null=True, blank=True)

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    main_campus = models.ForeignKey(Campus, unique=False)

