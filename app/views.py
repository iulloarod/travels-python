from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.http import request
from .models import User, Trip
from datetime import datetime, date
import bcrypt


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
        # username duplicate finder
        new_username_check = request.POST['username']
        registered_username = User.objects.filter(username=new_username_check)
        if registered_username :
            messages.error(request,"ERROR: This username already exists.")
            return redirect('/')
        # droping session info when register it's ok
        request.session['reg_name'] = ""
        request.session['reg_username'] = ""
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
                "name"  : f"{new_user.name}",
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
                    "name"  : f"{log_user.name}",
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
        trip_info = Trip.objects.filter(travels=user.id)

        not_this_user = User.objects.exclude(id=request.session['user']['id'])
        not_this_trip_info = Trip.objects.exclude(travels=user.id)

        context = {
            "username": user.username,
            "trip_info": trip_info,
            "other_trip": not_this_trip_info,
        }
        
        return render(request, 'travels.html', context)



def logout(request):
    request.session.flush()
    messages.success(request,'User logged out')
    return redirect("/")


def destination(request, id):
    trip = Trip.objects.get(id=int(id))
    #no me sale esto...
    trip_info = trip.travels.exclude()
    trip_user = trip_info.values("name")
    print(trip_user)
    context = {
        "destination" : trip.destination,
        "description" : trip.description,
        "planned_by" : trip.planned_by,
        "travel_from" : trip.date_from,
        "travel_to" : trip.date_to,
        "trip_user" : trip_user,
    }
    return render(request, 'destination.html', context)



def addtrip(request):
    if request.method =="GET":
        return render(request, 'addtrip.html')
    user = User.objects.get(id=request.session['user']['id'])
    if request.method == 'POST':
        #creating session to mantain input info if an error occurs
        request.session['reg_dest']     = request.POST['destination']
        request.session['reg_desc']    = request.POST['description']
        #data validation
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/travels/add')
        if datesValidator(request.POST['traveldatefrom'], request.POST['traveldateto']) == "False":
            messages.error(request,'Error : End date should be at least 1 day later than the start date')
            return redirect('/travels/add')
        # droping session info when register it's ok
        request.session['reg_dest']     = ""
        request.session['reg_desc']    = ""
        Trip.objects.create(
                            destination = request.POST['destination'],
                            description = request.POST['description'],
                            planned_by = user.name,                                                                    
                            date_from = request.POST['traveldatefrom'],
                            date_to = request.POST['traveldateto'],
                            )
        this_trip = Trip.objects.last()
        user.trips.add(this_trip.id)
    return redirect('/travels')

def join(request, id):
    trip = Trip.objects.get(id=int(id))
    user = User.objects.get(id=request.session['user']['id'])
    user.trips.add(trip.id)
    return redirect ("/travels")



def datesValidator(traveldatefrom, traveldateto):
# format to date time and then do a substraction
    start = traveldatefrom
    end = traveldateto
# convert to datetime
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
#calculating
    trip_duration = (start_date - end_date).days
    print (trip_duration)
    if trip_duration >= 1: 
        return "False"
    elif trip_duration == 0:
        return "False"
    else: 
        return "True"



