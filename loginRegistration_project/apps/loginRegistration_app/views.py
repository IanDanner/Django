# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime
from django.utils.crypto import get_random_string
from models import *
import bcrypt
# Create your views here.

def index(request):
    context = {
        "users" : User.objects.all()
    }
    return render(request,'loginRegistration_app/index.html',context)

def success(request, id):
    context = {
        "user" : User.objects.get(id=id)
    }
    return render(request,'loginRegistration_app/success.html',context)

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        User.objects.create(first_name = str(request.POST['first_name']),last_name= str(request.POST['last_name']),email= str(request.POST['email']),password=str(bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())))
        user = User.objects.get(email = request.POST['email'])
        id = user.id
    return redirect('/success/'+str(id))


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        user = User.objects.get(email = request.POST['email'])
        id = user.id
    return redirect('/success/'+str(id))