# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import re
import bcrypt


NAME_REGEX = re.compile(r'^[a-zA-Z]*$')

class RegManager(models.Manager):
    def validate(self, postData):
        error = []
        if len(postData['name']) < 4 or len(postData['username']) < 4:
            error.append("Name and Username must have at least 3 characters.")

        if len(postData['password']) < 8:
            error.append("Password must be at least 8 characters.")

        if postData['password'] != postData['confirm_pass']:
            error.append("Passwords don't match!")

        hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())

        existing_user = User.objects.filter(username=postData['username'])
        if len(existing_user) > 0:
            error.append("Username not available.")   
        
        if len(error) > 0:
            response = {
                'status': 'error',
                'data' : error
            }
            return response
        else:
            user = User.objects.create(name=postData['name'], username=postData['username'], password=hashed_pw)
            response = {
            'status': 'good',
            'data' : user
            }
            return response

    def auth(self, postData):
        error = []
        if len(postData['username']) < 4:
            error.append("Username must have at least 3 characters.")

        if len(postData['password']) < 8:
            error.append("Password must be at least 8 characters.")

        if postData['password'] != postData['confirm_pass']:
            error.append("Passwords don't match!")
        
        if len(error) > 0:
            response = {
                'status': 'error',
                'data' : error
            }
            return response
        else:
            retrieved_user = User.objects.filter(username=postData['username'])
            if len(retrieved_user) > 0:
                retrieved_user = retrieved_user[0]
                print retrieved_user.password
                if bcrypt.checkpw(postData['password'].encode(), retrieved_user.password.encode()):
                    print "MATCH"
                    response = {
                        'status' : 'good',
                        'data' : retrieved_user
                    }
                    return response
                else:
                    error.append("User and/or password don't match with our system.")
                    response = {
                        'status' : 'error',
                        'data': error
                    }
                    return response
            else:
                error.append("User and/or password don't match with our system.")
                response = {
                    'status' : 'error',
                    'data': error
                }
            return response
        return response

class TripManager(models.Manager):
    def validate(self, postData):
        error=[]
        if len(postData['destination']) < 1 or len(postData['description']) < 1 or len(postData['start']) < 1 or len(postData['end']) < 1:
            error.append("Fields cannot be blank.")

        if postData['start']> postData['end']:
            error.append("End time must be after start time.")
        
        if len(error) > 0:
            response = {
                'status': 'error',
                'data' : error
            }
            return response
        else:
            new_trip = Trip.objects.create(destination=postData['destination'], description=postData['description'], start_on=postData['start'], end_on=postData['end'])
            print postData['start']
            print postData['end']

            response = {
                'status': 'good',
                'data': new_trip
            }
            return response

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RegManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start_on = models.DateField(null=True)
    end_on = models.DateField(null=True)
    created_by = models.ForeignKey(User, related_name="created_trips", null=True)
    attendees = models.ManyToManyField(User, related_name="trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
