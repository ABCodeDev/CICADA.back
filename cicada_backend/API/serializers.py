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


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Organization
        fields = '__all__'


class AdministratorAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdministratorAccess
        fields = '__all__'


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Component
        fields = '__all__'


class TextFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TextField
        fields = '__all__'


class TimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Timer
        fields = '__all__'


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bill
        fields = '__all__'


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Form
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = '__all__'


class PossibleAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PossibleAnswer
        fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):
    response_content = None

    class Meta:
        model = models.Response
        fields = '__all__'


class UserNotificationFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserNotificationFeed
        fields = '__all__'


class PaymentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentResponse
        fields = '__all__'


class FormResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FormResponse
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = '__all__'


class UserComponentNotificationResponseSerializer(serializers.ModelSerializer):
    class Meta:
        id = serializers.IntegerField()

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = ('id', 'title', 'description', 'components', 'created', 'updated')

class NotificationComponentSerializer(serializers.ModelSerializer):
    components = ComponentSerializer(many=True)

    class Meta:
        model = models.Notification
        fields = ('id', 'title', 'description', 'components', 'created', 'updated')
