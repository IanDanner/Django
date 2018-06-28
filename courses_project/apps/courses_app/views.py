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
        "courses" : Course.objects.all()
    }
    return render(request,'courses_app/index.html',context)

def add(request):
    errors = Course.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        Course.objects.create(name = str(request.POST['name']),desc= str(request.POST['desc']))
    return redirect('/')

def destroy(request, id):
    context = {
        "course" : Course.objects.get(id=id)
    }
    return render(request,'courses_app/destroy.html',context)

def delete(request, id):
    course = Course.objects.get(id=id)
    course.delete()
    return redirect('/')
