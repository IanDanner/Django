# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-21 18:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booksAuthors_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book_author',
            old_name='author',
            new_name='authors',
        ),
        migrations.RenameField(
            model_name='book_author',
            old_name='book',
            new_name='books',
        ),
    ]