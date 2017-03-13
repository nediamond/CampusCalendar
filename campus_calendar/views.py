from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from models import *

# Todo: create_event view
# Todo: Add serialized/json event view for dynamic calendars


# Root view, shows main calendar of main campus if logged in
# Otherwise, login screen
def index(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.filter(user=request.user).first()
        return show_calendar(request, user_profile.main_campus.id)

    return render(request, 'login.html')


# Login data submission (POST) view, redirects to root url
@csrf_protect
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']  # Plaintext password submission is an issue USE HTTPS
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
    return redirect('/')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


# Todo: discuss whether users should have to be logged in to access this page
# Displays the main calendar for a given campus
@login_required
def show_calendar(request, campus_id):
    # Not the best way to decide this, might need a 'main_calendar' field
    main_calendar = CCalendar.objects.filter(campus_id=campus_id).first()
    events = Event.objects.filter(calendar=main_calendar).order_by('datetime')
    return render(request, 'display_calendar.html', {'calendar': main_calendar, 'events': events})


@login_required
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
    return render(request, 'create_event.html', {'org_id':org.id})


@csrf_protect
@login_required
def submit_event(request, org_id):
    if request.method != "POST":
        return HttpResponseForbidden()

    org = Organization.objects.filter(id=org_id).first()
    if not org or request.user not in org.administrators.all():
        return HttpResponseForbidden()
    main_calendar = CCalendar.objects.filter(campus=org.campus).first()  # See calendar comment up there ^^

    Event(name=request.POST['name'],
          location=request.POST['location'],
          datetime=request.POST['datetime'],
          calendar=main_calendar,
          organization=org).save()

    return redirect('/')