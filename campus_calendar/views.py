from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.core.files import File
from datetime import datetime
from collections import defaultdict

from models import *

# Todo: Add serialized/json event view for dynamic calendars?

# Root view, shows main calendar or campus select if no campus cookie set
def index(request):
    cid = request.session.get('cid', False)
    if not cid:
        return campus_list(request)
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

    if not request.session.get('cid', False):
        request.session['cid'] = campus_id

    days = defaultdict(list)
    for event in events:
        days[event.datetime.date()].append(event)
    print days
    days = [(v, days[v]) for v in dict(days)]
    days = sorted(days, key=lambda x: x[0])
    print days
    return render(request, 'display_calendar.html', {'calendar': main_calendar, 'days': days})

def campus_list(request):
    campuses = Campus.objects.all()
    return render(request, 'campus_list.html', {'campuses':campuses})


@login_required
def user_orgs(request):
    return render(request, 'my_orgs.html', {'orgs':request.user.organization_set.all()})


@csrf_protect
@login_required
def create_event(request, org_id):
    org = Organization.objects.filter(id=org_id).first()
    if not org or request.user not in org.administrators.all():
        return HttpResponseForbidden()
    return render(request, 'create_event.html', {'org_id': org.id, 'org_name': org.name})


@csrf_protect
@login_required
# Todo: tech debt, this view could probably use a django.forms.ModelForm
def submit_event(request, org_id):
    if request.method != "POST":
        return HttpResponseForbidden()

    org = Organization.objects.filter(id=org_id).first()
    if not org or request.user not in org.administrators.all():
        return HttpResponseForbidden()
    main_calendar = CampusCalendar.objects.filter(campus=org.campus).first()  # See calendar comment up there ^^

    new_event = Event(name=request.POST['name'],
                      location=request.POST['location'],
                      datetime=request.POST['datetime'],
                      calendar=main_calendar,
                      organization=org)
    new_event.save()

    if 'graphic' in request.FILES:
        # this may be vulnerable to js injection
        # Todo: extract file extension and randomize filename
        new_event.graphic.save(request.FILES['graphic'].name, File(request.FILES['graphic']))
        new_event.save()

    return redirect('/')

