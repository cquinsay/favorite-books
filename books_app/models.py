from django.db import models
from datetime import datetime
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def user_validator(self, postdata):
        EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postdata['first_name'])<2:
            errors['first_name']="First name must be longer than 2 characters!"
        if len(postdata['last_name'])<2:
            errors['last_name']="Last name must be longer than 2 characters!"
        if not EMAIL_REGEX.match(postdata['email']): 
            errors['email']="Email must be valid format!"
        if len(postdata['password'])<8:
            errors['password']="Password must be at least 8 characters!"
        if postdata['password'] != postdata['confirm_password']:
            errors['confirm_password']="Passwords do not match!"
        return errors

    def login_validator(self, postdata):
        errors = {}
        check = User.objects.filter(email=postdata['login_email'])
        if not check:
            errors['login_email'] = "Email has not been registered!"
        else:
            if not bcrypt.checkpw(postdata['login_password'].encode(), check[0].password.encode()):
                errors['login_email'] = "Email and password do not match!"
        return errors


class BookManager(models.Manager):
    def book_validator(self, postdata):
        errors = {}
        if len(postdata['title'])<1:
            errors['title']="Title is required!"
        if len(postdata['description'])<5:
            errors['description']="Description must be at least 5 characters!"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    book_adder = models.ForeignKey(User, related_name="books", on_delete = models.CASCADE)
    favoriter = models.ManyToManyField(User, related_name="favorited_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=BookManager()

# Create your models here.
