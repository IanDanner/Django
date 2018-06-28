# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors['first_name'] = "User first_name cannot be empty"
        if any(char.isdigit() for char in postData['first_name']) == True:
            errors['first_name'] = "User first_name cannot contain numbers"

        if len(postData['last_name']) < 1:
            errors['last_name'] = "User last_name cannot be empty"
        if any(char.isdigit() for char in postData['last_name']) == True:
            errors['last_name'] = "User last_name cannot contain numbers"

        if len(postData['email']) < 1:
            errors['email'] = "User email cannot be empty"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "User email is not a valid email"
        
        for user in User.objects.all():
            if user.email == postData['email']:
                errors['email'] = "User email is already registered"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be more than 8 characters!"
        if postData['password'] != postData['confirm_pw']:
            errors['password'] = "Password must be the same as Confirm PW"

        return errors
    def login_validator(self, postData):
        errors = {}
        if len(User.objects.filter(email = postData['email'])) < 1:
            errors['email'] = "User email not found"
            return errors
        get = User.objects.get(email= postData['email'])
        if bcrypt.checkpw(postData['password'].encode(), get.password.encode()) == False:
            errors['password'] = "User password incorrect"
        return errors
    def book_validator(self, postData):
        errors = {}
        for book in Book.objects.all():
            if book.title == postData['title']:
                errors['title'] = "Book has already been registered"
        for author in Author.objects.all():
            if author.name == postData['new_author']:
                errors['author'] = "Author has already been registered"
        if len(postData['title']) < 1:
            errors['title'] = "Book title cannot be empty"
        if len(postData['new_author']) < 1 and postData['known_author'] == "Choose Author":
            errors['author'] = "Book has no author"
        if len(postData['new_author']) > 1 and postData['known_author'] != "Choose Author":
            errors['author'] = "Cannot add two authors"
        if len(postData['review']) < 1:
            errors['review'] = "Book has no review"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {}, {}, {}, {}>".format(self.first_name,self.last_name,self.email,self.password)
    

class Author(models.Model):
    name = models.CharField(max_length=255)
    def __repr__(self):
        return "<Author object: {}>".format(self.name)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books_written")
    def __repr__(self):
        return "<Book object: {}, {}>".format(self.title,self.author,self.reviews)

class Review(models.Model):
    review = models.TextField()
    rating = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    reviewer = models.ForeignKey(User, related_name="reviews_made")
    book_reviewed = models.ForeignKey(Book, related_name="reviews")
    def __repr__(self):
        return "<User object: {}, {}, {}, {}>".format(self.review,self.rating,self.created_at,self.reviewer,self.book_reviewed)
    


















