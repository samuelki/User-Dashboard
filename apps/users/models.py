from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    adminCreated = False

    # validates the POST data before updating/creating user
    def validator(self, form):
        errors = {}

        # validate first name
        if len(form['first_name']) < 2 or not form['first_name'].isalpha():
            if len(form['first_name']) < 2:
                errors['first_name_length'] = "First name must be at least 2 characters."
            if not form['first_name'].isalpha():
                errors['first_name_alpha'] = "First name can only contain letters."

        # validate last name
        if len(form['last_name']) < 2 or not form['last_name'].isalpha():
            if len(form['last_name']) < 2:
                errors['last_name_length'] = "Last name must be at least 2 characters."
            if not form['last_name'].isalpha():
                errors['last_name_alpha'] = "Last name can only contain letters."

        # validate email
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = "Invalid email address."
        try:
            self.get(email=form['email'])
            errors['email'] = "Email is already in use."
        except:
            pass

        # validate password
        if len(form['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long."
        
        if form['password'] != form['confirm_pw']:
            errors['confirm_pw'] = "Password do not match."

        return errors

    def pw_validator(self, form):
        errors = {}
        if len(form['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        if form['password'] != form['confirm_pw']:
            errors['confirm_pw'] = "Passwords do not match"
            
        return errors 

    def update_validator(self, form):
        errors = {}

        # validate first name
        if len(form['first_name']) < 2 or not form['first_name'].isalpha():
            if len(form['first_name']) < 2:
                errors['first_name_length'] = "First name must be at least 2 characters."
            if not form['first_name'].isalpha():
                errors['first_name_alpha'] = "First name can only contain letters."

        # validate last name
        if len(form['last_name']) < 2 or not form['last_name'].isalpha():
            if len(form['last_name']) < 2:
                errors['last_name_length'] = "Last name must be at least 2 characters."
            if not form['last_name'].isalpha():
                errors['last_name_alpha'] = "Last name can only contain letters."
        
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = "Invalid email address."
        try:
            self.get(email=form['email'])
            errors['email'] = "Email is already in use."
        except:
            pass

        return errors

    # first user created is an admin, update adminCreated so create method knows what level to assign each user
    def get_user_count(self):
        return self.all().count()

    def create_admin(self):
        if self.get_user_count() > 0:
            self.adminCreated = True
        else:
            self.adminCreate = False

    def create_user(self, form):
        if not self.adminCreated:
            self.create_admin()
        if not self.adminCreated:
            user_level = 9
            self.adminCreated = True
        else:
            user_level = 0
        pw_hash = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
        user = self.create(
            first_name=form['first_name'],
            last_name=form['last_name'],
            email=form['email'],
            password=pw_hash,
            user_level=user_level
        )
        return user

    def login(self, form):
        # find the user with the given email
        user = self.filter(email=form['email'])
        if len(user) > 0:
            # email found, check pw 
            if bcrypt.checkpw(form['password'].encode(), user[0].password.encode()):
                # email and pw match
                return(True, user[0].id, user[0].user_level)
            else:
                # pw does not match
                return(False, "Incorrect email and/or password", None)
        else:
            # email not found
            return(False, "Account does not exist", None)


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=500)
    user_level = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def update_pw(self, form):
        pw_hash = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
        self.password = pw_hash
        self.save()

    def update_level(self, form):
        self.user_level = form['level']
        self.save()

class Message(models.Model):
    message = models.TextField()
    from_user = models.ForeignKey(User, related_name="messages_sent")
    for_user = models.ForeignKey(User, related_name="messages_received")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, related_name="user_comments")
    message = models.ForeignKey(Message, related_name="message_comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)