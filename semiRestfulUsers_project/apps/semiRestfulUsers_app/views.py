# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime
from django.utils.crypto import get_random_string
from models import *
# Create your views here.

def index(request):
    context = {
        "users" : User.objects.all()
    }
    return render(request,'semiRestfulUsers_app/index.html',context)


def new(request):
    return render(request,'semiRestfulUsers_app/new.html')

def edit(request, id):
    request.session['user_id'] = id
    context = {
        "user" : User.objects.get(id=id)
    }
    return render(request,'semiRestfulUsers_app/edit.html',context)

def show(request, id):
    context = {
        "user" : User.objects.get(id=id)
    }
    return render(request,'semiRestfulUsers_app/show.html',context)

def create(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/users/create')
    else:
        User.objects.create(first_name = str(request.POST['first_name']),last_name= str(request.POST['last_name']),email= str(request.POST['email']))
    return redirect('/users')

def destroy(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('/users')

def update(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/users/edit'+int(request.session['user_id']))
    else:
        user = User.objects.get(request.session['user_id'])
        user.first_name = str(request.POST['first_name'])
        user.last_name = str(request.POST['last_name'])
        user.email = str(request.POST['email'])
        user.save()
    return redirect('/users')