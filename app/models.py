from django.db import models
import re	
import datetime
from datetime import date


class TripManager(models.Manager):
    def trip_validator(self, postData):    
        errors = {}

        CHAR_REGEX = re.compile(r'^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$')

        if len(postData['destination'])<6:
            errors['destination'] = "Destination must be at least 6 characters long"

        if len(postData['description'])<6:
            errors['description'] = "Description must be at least 6 characters long"
                
        return errors


class Trip (models.Model):
    destination = models.CharField(max_length = 255)
    description = models.TextField()
    planned_by = models.CharField(max_length = 255, null=True)
    date_from = models.DateField()
    date_to = models.DateField()
    objects = TripManager()
    #travels it's a list of trips asociated to a user


class UserManager(models.Manager):
    def user_validator(self, postData):    
        errors = {}

        CHAR_REGEX = re.compile(r'^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$')

        if len(postData['name'])<3:
            errors['name'] = "Name must be at least 3 characters long"

        if len(postData['username'])<3:
            errors['username'] = "Username must be at least 3 characters long"

        if not CHAR_REGEX.match(postData['name']):
            errors['name'] = "First Name accepts only letters without a space at the beginning"

        if not CHAR_REGEX.match(postData['username']):
            errors['username'] = "Last Name accepts only letters without a space at the beginning"

        if len(postData['password'])<8:
            errors['password'] = "Password must have at least 8 characters!"

        if postData['password'] != postData['reppassword']:
            errors['password'] = "Passwords are not identical!"
        
        return errors


class User (models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    trips= models.ManyToManyField("Trip", related_name='travels')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return (f"Id #{self.id} Name : {self.name} username : {self.username}")
    def __str__(self):
        return (f"Id #{self.id} Name : {self.name} username : {self.username}")



