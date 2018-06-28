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
    return render(request,'beltReviewer_app/index.html',context)

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        User.objects.create(
            first_name = str(request.POST['first_name']),
            last_name = str(request.POST['last_name']),
            email = str(request.POST['email']),
            password = str(bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
            )
        user = User.objects.get(email = request.POST['email'])
        request.session['user_id'] = user.id
    return redirect('/list_books')


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        user = User.objects.get(email = request.POST['email'])
        request.session['user_id'] = user.id
    return redirect('/list_books')

def list_books(request):
    if 'user_id' not in request.session:
        return redirect('/')
    count = len(Book.objects.all())
    context = {
        "user" : User.objects.get(id=request.session['user_id']),
        "last_books" : [Book.objects.get(id = count), Book.objects.get(id = count-1), Book.objects.get(id = count-2)],
        "books" : Book.objects.order_by("title")
    }
    return render(request,'beltReviewer_app/list_books.html',context)

def new_book(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "authors" : Author.objects.all()
    }
    return render(request,'beltReviewer_app/new_book.html',context)

def add_book(request):
    errors = User.objects.book_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/new_book')
    else:
        if len(request.POST['new_author']) > 1 and request.POST['known_author'] == "Choose Author":
            author = request.POST['new_author']
        elif len(request.POST['new_author']) < 1 and request.POST['known_author'] != "Choose Author":
            author = request.POST['known_author']
        author_name = Author.objects.create(
            name= str(author),
            )
        new_book = Book.objects.create(
            title = str(request.POST['title']),
            author= author_name
            )
        new_review = Review.objects.create(
            review = str(request.POST['review']),
            rating = str(request.POST['rating']),
            reviewer = User.objects.get(id=request.session['user_id']),
            book_reviewed = new_book
            )
    return redirect('/list_books')

def view_book(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    request.session['book_id'] = id
    context = {
        "book" : Book.objects.get(id=id),
        "reviews" : Review.objects.filter(book_reviewed = Book.objects.get(id=id)),
        "current_user" : request.session['user_id']
    }
    return render(request,'beltReviewer_app/view_book.html',context)

def add_review(request):
    new_review = Review.objects.create(
        review = str(request.POST['review']),
        rating = str(request.POST['rating']),
        reviewer = User.objects.get(id=request.session['user_id']),
        book_reviewed = Book.objects.get(id=request.session['book_id']),
        )
    return redirect('/view_book/'+str(request.session['book_id']))

def view_user(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "user" : User.objects.get(id=request.session['user_id']),
        "reviews" : Review.objects.filter(reviewer = User.objects.get(id=id)),
        "count" : len(Review.objects.filter(reviewer = User.objects.get(id=id)))
    }
    return render(request,'beltReviewer_app/view_user.html',context)

def delete_review(request, id):
    remove = Review.objects.get(id=id)
    remove.delete()
    return redirect('/view_book/'+str(request.session['book_id']))













