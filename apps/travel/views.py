# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import formats
import time


def index(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return render(request, 'travel/index.html')

def register_user(request):
    if request.method == "POST":
        potential_errors = User.objects.validate(request.POST)
        if potential_errors['status'] == "error":
            for error in potential_errors['data']:
                messages.error(request, error)
            return redirect('/')
        else:
            user_id = potential_errors['data'].id
            username = potential_errors['data'].username
            print username
            request.session['user_id'] = user_id
            return redirect('/travels')
    else:
        return redirect('/')

def login_user(request):
    if request.method == "POST":
        potential_errors = User.objects.auth(request.POST)
        if potential_errors['status'] == "error":
            for error in potential_errors['data']:
                messages.error(request, error)
            return redirect('/')
        else:
            user_id = potential_errors['data'].id
            username = potential_errors['data'].username
            print username
            request.session['user_id'] = user_id
            return redirect('/travels')
    else:
        return redirect('/')

def logout(request):
    del request.session['user_id']
    return redirect('/')

def add(request):
    context = {
    'date' : time.strftime('%Y-%m-%d'),
    'id' : request.session['user_id']
    }
    return render(request, 'travel/add.html', context)

def add_trip(request):
    if request.method =="POST":
        potential_errors = Trip.objects.validate(request.POST)
        if potential_errors['status'] == "error":
            for error in potential_errors['data']:
                messages.error(request, error)
            return redirect('/travels/add')
        else:
            trip_id = potential_errors['data'].id
            user = request.session['user_id']
            user_int = User.objects.get(id=user)
            trip = Trip.objects.get(id=trip_id)
            trip.created_by = user_int
            trip.attendees.add(user)
            trip.save()
            return redirect('/travels')
    else:
        return redirect('/travels/add')

def travels(request):
    if 'user_id' in request.session:

        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        trips = User.objects.get(id=user_id).trips.all()

        all_trips = Trip.objects.exclude(attendees__id=user_id)

        context = {
            'user': user,
            'trips': trips,
            'all_trips': all_trips
        }
        return render(request, 'travel/travel.html', context)
    else:
        return redirect('/')

def destination(request, trip_id):

    user_id = request.session['user_id']
    trip_id = trip_id
    trip = Trip.objects.get(id=trip_id)

    attendees = Trip.objects.get(id=trip_id).attendees.exclude(username=trip.created_by.username)

    context = {
        'trip_id': trip_id,
        'trip_info': trip,
        'attendees': attendees
    }
    return render(request, 'travel/single.html', context)

def join(request, trip_id):
    user_id = request.session['user_id']
    trip_id = trip_id

    trip = Trip.objects.get(id=trip_id)
    trip.attendees.add(user_id)
    trip.save()
    return redirect('/travels')