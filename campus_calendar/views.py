from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from models import *


def index(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.filter(user=request.user).first()
        return show_calendar(request, user_profile.main_campus.id)

    return render(request, 'login.html')


@csrf_protect
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']  # Plaintext password submission might be an issue? maybe not with https
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
    return redirect('/')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def show_calendar(request, campus_id):
    main_calendar = CCalendar.objects.filter(campus_id=campus_id).first()  # Not the best way to do this
    events = Event.objects.filter(calendar=main_calendar)
    return render(request, 'display_calendar.html', {'calendar': main_calendar, 'events': events})

@login_required
def create_event(request):
    return 'aylmao'