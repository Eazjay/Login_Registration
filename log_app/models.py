from django.db import models
import re

class User_Manager(models.Manager):
    def registration_validator(self, form_data):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(form_data['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters."
        if len(form_data['first_name']) == 0:
            errors['first_name'] = "Please enter first name"
        if len(form_data['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters."
        if len(form_data['last_name']) == 0:
            errors['last_name'] = "Please enter last name"
        if not email_regex.match(form_data['reg_email']):           
            errors['reg_email'] = "Invalid email address."
        if len(form_data['reg_email']) == 0:
            errors['reg_email'] = "Please enter an email address"
        if len(form_data['reg_password']) < 8:
            errors['reg_password'] = "Password must be at least 8 characters."
        if len(form_data['reg_password']) == 0:
            errors['reg_password'] = "Please enter a password"
        if form_data['reg_password'] != form_data['confirm_password']:
            errors['confirm_password'] = "Password doesn't match."
        return errors

    def login_validator(self, form_data):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(form_data['log_email']):           
            errors['log_email'] = "Please enter a valid email address."
        if len(form_data['log_email']) == 0:
            errors['log_email'] = "Please enter an email address."
        if len(form_data['log_password']) == 0:
            errors['log_password'] = "Please enter a password."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = User_Manager()