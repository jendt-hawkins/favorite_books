from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):

        errors = {}

        if len(postData['first_name'])<2:
            errors['first_name'] = "First name must be at least 2 characters"

        if len(postData['last_name'])<2:
            errors['last_name'] = "Last name must be at least 2 characters"

        if len(postData['email'])<1:
            errors['email'] = "Email cannot be blank"
        elif not EMAIL_REGEX.match(postData['email']):               
            errors['email'] = "Invalid email address"

        if len(postData['password'])<8:
            errors['password'] = "Password must be at least 8 characters"

        if postData['password'] != postData['confirm']:
            errors['passwords'] = "Passwords must match"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()


class BookManager(models.Manager):
    def book_validator(self, postData):

        errors = {}

        if len(postData['title'])<1:
            errors['title'] = "Title is required"

        if len(postData['description'])<5:
            errors['description'] = "Description must be at least 5 characters long"

        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete = models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = BookManager()