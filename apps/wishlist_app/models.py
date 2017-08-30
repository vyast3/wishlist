from __future__ import unicode_literals
import re
import bcrypt
from django.db import models

# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []
        # check DB for post_data['email']
        if len(self.filter(username=post_data['username'])) > 0:
            # check this user's password
            user = self.filter(username=post_data['username'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('username/password incorrect')
        else:
            errors.append('username/password incorrect')

        if errors:
            return errors
        return user

    def validate_registration(self, post_data):
        errors = []
        # check length of name fields
        if len(post_data['name']) < 3:
            errors.append("name field must be at least 3 characters")
        # check length of name password
        if len(post_data['password']) < 8:
            errors.append("password must be at least 8 characters")

        if len(post_data['username']) < 1:
            errors.append("username cannot be empty")
        # check name fields for letter characters            
        if not re.match(NAME_REGEX, post_data['name']):
            errors.append('name field must be letter characters only')
        # check emailness of email
        # if not re.match(EMAIL_REGEX, post_data['email']):
        #     errors.append("invalid email")
        # check uniqueness of email
        if len(User.objects.filter(username=post_data['username'])) > 0:
            errors.append("username already in use")
        # check password == password_confirm
        if post_data['password'] != post_data['password_confirm']:
            errors.append("passwords do not match")

        if not errors:
            # make our new user
            # hash password
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                name=post_data['name'],
                username=post_data['username'],
                date_hired=post_data['date_hired'],
                password=hashed
            )
            return new_user
        return errors


class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    date_hired = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return self.name

class List(models.Model):
    product_name = models.CharField(max_length=100)
    wished_by = models.ManyToManyField(User, related_name = "wish")
    added_by = models.ForeignKey(User,related_name = "add")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)