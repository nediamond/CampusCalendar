from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.core.files import File
from django.utils.crypto import get_random_string

from datetime import datetime
from collections import defaultdict
import os

from models import *


# Root view, shows main calendar or campus select if no campus cookie set
def index(request):
    cid = request.session.get('cid', False)
    if not cid:
        return redirect('/campus_list/')
    return show_calendar(request, cid)


# Login data submission (POST) view, redirects to root url
@csrf_protect
def login_post_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']  # Plaintext password submission is an issue, FORCE HTTPS
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        return redirect('/')
    else:
        return redirect('/login/')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


def login_page(request):
    return render(request, 'login.html')


# Displays the main calendar for a given campus
def show_calendar(request, campus_id):
    # Not the best way to decide this, might need a 'main_calendar' field
    # Or maybe theres just one calendar per university in which case they can be the same object
    main_calendar = CampusCalendar.objects.filter(campus_id=campus_id).first()
    events = Event.objects.filter(calendar=main_calendar, datetime__gte=datetime.now()).order_by('datetime')

    request.session['cid'] = campus_id

    days = defaultdict(list)
    for event in events:
        days[event.datetime.date()].append(event)

    days = [(v, days[v]) for v in dict(days)]
    days = sorted(days, key=lambda x: x[0])

    return render(request, 'display_calendar.html', {'calendar': main_calendar, 'days': days})


def campus_list(request):
    campuses = Campus.objects.all()
    return render(request, 'campus_list.html', {'campuses':campuses})


@login_required
def event_manager(request):
    events = Event.objects.filter(organization__in=request.user.organization_set.all(),
                                  datetime__gte=datetime.now()).order_by('datetime')
    return render(request, 'event_manger.html', {'events':events})


@login_required
def delete_event(request, event_id):
    event = Event.objects.filter(id=event_id).first()
    if not event or request.user not in event.organization.administrators.all():
        return HttpResponseForbidden()

    event.delete()
    return redirect('/event_manager/')


# Todo: tech debt, this view could probably use a django.forms.ModelForm
@csrf_protect
@login_required
def create_event(request):
    if request.method == "GET":
        orgs = Organization.objects.filter(administrators=request.user)
        if len(orgs) < 1:
            return HttpResponseForbidden()
        return render(request, 'create_event.html', {'orgs': orgs})

    elif request.method == "POST":
        org = Organization.objects.filter(id=int(request.POST['org'])).first()
        if not org or request.user not in org.administrators.all():
            return HttpResponseForbidden()

        main_calendar = CampusCalendar.objects.filter(campus=org.campus).first()  # See calendar comment up there ^^
        event_dt = datetime.strptime(request.POST['datetime'], "%Y-%m-%dT%H:%M")
        event_endt = datetime.strptime(request.POST['endtime'], "%H:%M")

        # Should handle this in a better/safer way, maybe use some js
        if event_dt.time() < event_endt.time():
            new_event = Event(name=request.POST['name'],
                              location=request.POST['location'],
                              datetime=event_dt,
                              endtime=event_endt,
                              calendar=main_calendar,
                              organization=org,
                              description=request.POST['description'])
            new_event.save()
        else:
            orgs = Organization.objects.filter(administrators=request.user)
            if len(orgs) < 1:
                return HttpResponseForbidden()
            return render(request, 'create_event.html', {'orgs': orgs})

        if 'graphic' in request.FILES:
            _, extension = os.path.splitext(request.FILES['graphic'].name)
            new_event.graphic.save(get_random_string(length=16)+extension, File(request.FILES['graphic']))
            new_event.save()

        return redirect('/event_manager/')

    else:
        return HttpResponseForbidden()


@csrf_protect
@login_required
def edit_event(request, event_id):
    if request.method == "GET":
        orgs = Organization.objects.filter(administrators=request.user)
        event = Event.objects.filter(id=event_id).first()

        if len(orgs) < 1 or not event:
            return HttpResponseForbidden()

        return render(request, 'edit_event.html', {'orgs': orgs, 'event':event})

    elif request.method == "POST":
        org = Organization.objects.filter(id=int(request.POST['org'])).first()
        event = Event.objects.filter(id=event_id).first()
        if not org or request.user not in org.administrators.all() or not event:
            return HttpResponseForbidden()

        event_dt = datetime.strptime(request.POST['datetime'], "%Y-%m-%dT%H:%M")
        event_endt = datetime.strptime(request.POST['endtime'], "%H:%M")

        # Should handle this in a better/safer way, maybe use some js
        # Also needs an error message when this if statement is false
        if event_dt.time() < event_endt.time():
            event.name = request.POST['name']
            event.location = request.POST['location']
            event.datetime = event_dt
            event.endtime = event_endt
            event.organization = org
            event.description = request.POST['description']

            event.save()

            if 'graphic' in request.FILES and request.FILES['graphic']:
                if event.graphic:
                    event.graphic.delete()

                _, extension = os.path.splitext(request.FILES['graphic'].name)
                event.graphic.save(get_random_string(length=16)+extension, File(request.FILES['graphic']))
                event.save()

        return redirect('/event_manager/')

    else:
        return HttpResponseForbidden()



