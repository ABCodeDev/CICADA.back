from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#User Profile Related

class Organization(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField (max_length=35)

class AdministratorAccess(models.Model):
    id = models.AutoField(primary_key=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    ktp_no = models.CharField(max_length=17)
    npwp_no = models.CharField(max_length=15, blank=True)
    phone_no = models.CharField(max_length=11)
    birth_date = models.DateField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    access = models.ForeignKey(AdministratorAccess, on_delete=models.CASCADE)

#Notifications and Component
class Component(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    singleuse = models.BooleanField(default=False)
    description = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    components = models.ManyToManyField(Component)
    access = models.ForeignKey(AdministratorAccess, on_delete=models.CASCADE)

class Text_Field(models.Model):
    component = models.OneToOneField(Component,on_delete=models.CASCADE)
    content = models.TextField()

class Timer(models.Model):
    component = models.OneToOneField(Component,on_delete=models.CASCADE)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False)

class Bill(models.Model):
    component = models.OneToOneField(Component,on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=12, decimal_places=0)

class Form(models.Model):
    component = models.OneToOneField(Component, on_delete=models.CASCADE)
    due_date = models.DateTimeField(auto_now=False, auto_now_add=False)

class Question(models.Model):
    QUESTION_TYPES = (

    )
    form = models.ForeignKey(Form,on_delete=models.CASCADE)
    type = models.CharField(max_length=1,choices=QUESTION_TYPES)
    regex = models.CharField(max_length=100)
    question = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    is_multivalue_question = models.BooleanField(default=False)

class Possible_answer(models.Model):
    question = models.ForeignKey(Question)
    possible_answer = models.CharField(max_length=200)

#User Response

class Response(models.Model): pass

class UserNotificationFeed(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    response = models.ForeignKey(Response, on_delete=models.CASCADE)

class Payment_response(models.Model):
    is_fulfilled = models.BooleanField(default=False)
    date_fulfilled = models.DateTimeField(auto_now=False,auto_now_add=False)
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)

class Form_Response(models.Model):
    response = models.ForeignKey(Response)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Answer(models.Model):
    form_response = models.ForeignKey(Form_Response,on_delete=models.CASCADE)
    answer = models.ForeignKey(Question)