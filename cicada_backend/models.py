from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# Create your models here.

#User Profile Related

class Organization(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField (max_length=35,null=True,blank=True)

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
    notifications = models.ManyToManyField('Notification', through='UserNotificationFeed')
    responses = models.ManyToManyField('Response', through='UserComponentNotificationResponse')

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

class TextField(models.Model):
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

class PossibleAnswer(models.Model):
    question = models.ForeignKey(Question)
    possible_answer = models.CharField(max_length=200)

#User Response

class Response(models.Model):
    RESPONSE_TYPE = (
        ('P','Payment'),
        ('F','Form')
    )
    type = models.CharField(max_length=1,choices=RESPONSE_TYPE)

class UserNotificationFeed(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)

class PaymentResponse(models.Model):
    is_fulfilled = models.BooleanField(default=False)
    date_fulfilled = models.DateTimeField(auto_now=False,auto_now_add=False)
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)

class FormResponse(models.Model):
    response = models.ForeignKey(Response)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Answer(models.Model):
    form_response = models.ForeignKey(FormResponse,on_delete=models.CASCADE)
    answer = models.ForeignKey(Question)

class UserComponentNotificationResponse(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    response = models.ForeignKey(Response, on_delete=models.CASCADE)

# This code is triggered whenever a new user has been created and saved to the database

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)