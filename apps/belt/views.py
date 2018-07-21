from django.shortcuts import render, redirect
from apps.belt.models import *
from django.contrib import messages 

def index(request): 
    return redirect("home")

def main(request): 
    return render(request, "belt/index.html")

def register_user(request):
    request.session['data'] = {
        "alias": request.POST['alias'],
        "name": request.POST['name'],
        "email": request.POST['email'],
        "dob": request.POST['dateOfBirth'],
    }
    errors = User.objects.validate(request.POST)
    #registration failure
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect("home")
        #registration success
    else:
        User.objects.register(request.POST)
        request.session.clear()
        id = User.objects.get(email=request.POST['email']).id
        request.session['data'] = {
            "id": id,
            "alias": request.POST['alias'],
            'logged_in': True
        }
        return redirect("wall")

def login_user(request):
    user = User.objects.validate_login(request.POST)
    if user:
        alias =User.objects.get(id=user).alias
        request.session['data'] = {
            'id': user,
            'alias': alias,
            'logged_in': True
        }
        return redirect("wall")
    else:
        request.session['data'] = {
            'loginEmail': request.POST['loginEmail'],
            'loginError': "unable to login"
        }
        return redirect("home")

def access_wall(request):
    if 'data' in request.session:
        context = {
            "friends": User.objects.filter(relationships__id=request.session['data']['id']).exclude(id=request.session['data']['id']),
            "nonFriends": User.objects.all().exclude(relationships__id=request.session['data']['id']).exclude(id=request.session['data']['id'])
        }
        print(context)
        return render(request, "belt/wall.html", context)
    return redirect("home")

def display_user(request, user_id): 
    context = {
        "user": User.objects.get(id=user_id)
    }
    return render(request, "belt/profile.html", context)

def add(request, user_id):
    Relationship.objects.create(from_user_id=user_id, to_user_id=request.session['data']['id'])
    Relationship.objects.create(from_user_id=request.session['data']['id'], to_user_id=user_id)


    return redirect("wall")

def remove(request, user_id): 
    Relationship.objects.filter(from_user_id=user_id, to_user_id=request.session['data']['id']).delete()
    Relationship.objects.filter(from_user_id=request.session['data']['id'], to_user_id=user_id).delete()
    return redirect("wall")

def logout(request):
    request.session.clear()
    return redirect("home")


