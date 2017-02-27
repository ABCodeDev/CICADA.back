from django.contrib.auth.models import User, Group
from rest_framework import serializers
import cicada_backend.models

models = cicada_backend.models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'id',
            'password',
            'first_name',
            'last_name',
            'email',
            'username'
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.Profile
        fields = '__all__'


class Organization(serializers.ModelSerializer):
    class Meta:
        model = models.Organization
        fields = '__all__'


class AdministratorAccess(serializers.ModelSerializer):
    class Meta:
        model = models.AdministratorAccess
        fields = '__all__'


class Component(serializers.ModelSerializer):
    class Meta:
        model = models.Component
        fields = '__all__'


class Notification(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = '__all__'


class TextField(serializers.ModelSerializer):
    class Meta:
        model = models.TextField
        fields = '__all__'


class Timer(serializers.ModelSerializer):
    class Meta:
        model = models.Timer
        fields = '__all__'


class Bill(serializers.ModelSerializer):
    class Meta:
        model = models.Bill
        fields = '__all__'


class Form(serializers.ModelSerializer):
    class Meta:
        model = models.Form
        fields = '__all__'


class Question(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = '__all__'


class PossibleAnswer(serializers.ModelSerializer):
    class Meta:
        model = models.PossibleAnswer
        fields = '__all__'


class UserNotificationFeed(serializers.ModelSerializer):
    class Meta:
        model = models.UserNotificationFeed
        fields = '__all__'


class PaymentResponse(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentResponse
        fields = '__all__'


class FormResponse(serializers.ModelSerializer):
    class Meta:
        model = models.FormResponse
        fields = '__all__'


class Answer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = '__all__'


class UserComponentNotificationResponse(serializers.ModelSerializer):
    class Meta:
        model = models.UserComponentNotificationResponse
        fields = '__all__'
