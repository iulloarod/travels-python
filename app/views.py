from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.http import request
from .models import User, Trip
from datetime import datetime, date
import bcrypt
from itertools import chain


def index(request):
    return render(request, 'index.html')


def registration(request):
    if request.method == 'POST':
        #creating session to mantain input info if an error occurs
        request.session['reg_name']     = request.POST['name']
        request.session['reg_username']    = request.POST['username']
        #data validation
        errors = User.objects.user_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        # droping session info when register it's ok
        request.session['reg_name'] = ""
        request.session['reg_username'] = ""
        request.session['reg_email'] = ""
        #  hashing the password
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print (pw_hash)
        # having checked for erorrs, checked if the email already existed and hashed the password, it now creates the new user:
        new_user = User.objects.create(
                                        name = request.POST['name'],
                                        username=request.POST['username'],
                                        password=pw_hash,                                      
                                        )
        # creating session.user to use later
        request.session['user'] = {
                "id"    : new_user.id,
                "name"  : f"{new_user.username}",
            }
        messages.success(request, "Welcome User!")
        return redirect("/travels")


def login(request):
    if request.method == "POST":
        print(request.POST)
        user = User.objects.filter(username=request.POST['username'])
        if user:
            log_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
                user_logged = {
                    "id"    : log_user.id,
                    "name"  : f"{log_user.username}",
                }
                request.session['user'] = user_logged
                messages.success(request, "Loged.")
                return redirect("/travels")
            else:
                messages.error(request, "Username or Password incorrect.")
        else:
            messages.error(request, "Username or Password incorrect.")
    return redirect("/")


def travels(request):
    if 'user' not in request.session:
        return redirect("/login")
    else:
        user = User.objects.get(id=request.session['user']['id'])
        trip_info = Trip.objects.all()

        context = {
            "name": user.name,
            "destination": trip_info.destination,
            "tsd": trip_info.date_from,
            "ted": trip_info.date_to,
            "plan": trip_info.planned_by,
        }
        
        return render(request, 'travels.html', context)



def logout(request):
    request.session.flush()
    messages.success(request,'User logged out')
    return redirect("/")


def destination(request, id):
    trip = Trip.objects.get(id=int(id))
    context = {
        "destination" : trip.destination,
        "description" : trip.description,
        "planned_by" : trip.planned_by,
        "travel_from" : trip.date_from,
        "travel_to" : trip.date_to,
        "others" : trip.travels,
    }
    return render(request, 'destination.html', context)



def addtrip(request):
    user = User.objects.get(id=request.session['user']['id'])
    if request.method == "POST":
        new_trip = Trip.objects.create(
                                            destination = request.POST['destination'],
                                            description = request.POST['description'],
                                            planned_by = user.username,                                                                    
                                            date_from = request.POST['traveldatefrom'],
                                            date_to = request.POST['traveldateto'],
                                            )
    return render(request, 'addtrip.html')