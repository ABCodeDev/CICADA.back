from django.db import models

# Create your models here.

#Notifications and Component
class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

class Component(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    singleuse = models.BooleanField(default=False)
    description = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Text_Field(models.Model):
    id_component = models.OneToOneField(Component,on_delete=models.CASCADE)
    content = models.TextField()

class Timer(models.Model):
    id_component = models.OneToOneField(Component,on_delete=models.CASCADE)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False)

class Bill(models.Model):
    id_component = models.OneToOneField(Component,on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=None, decimal_places=None)

class Form(models.Model):
    id_component = models.OneToOneField(Component, on_delete=models.CASCADE)
    due_date = models.DateTimeField(auto_now=False, auto_now_add=False)

class Question(models.Model):
    QUESTION_TYPES = (

    )
    type = models.CharField(max_length=1,choices=QUESTION_TYPES)
    regex = models.CharField(max_length=100)
    question = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    is_multivalue_question = models.BooleanField(default=False)

class Possible_answer(models.Model):
    id_question = models.ForeignKey(Question)
    possible_answer = models.CharField(max_length=200)

#User Response

class Response(models.Model): pass

class Payment_response(models.Model):
    is_fulfilled = models.BooleanField(default=False)
    date_fulfilled = models.DateTimeField(auto_now=False,auto_now_add=False)

class Form_Response(models.Model):
    id_response = models.ForeignKey(Response)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Answer(models.Model):
    id_form_response = models.ForeignKey(Form_Response,on_delete=models.CASCADE)
    id_answer = models.ForeignKey(Question)