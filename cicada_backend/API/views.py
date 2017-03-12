from __future__ import print_function
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import generics
from cicada_backend.models import *
from cicada_backend.API.serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
import json


class UserMixin:
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (AllowAny,)


class UserList(UserMixin, generics.ListCreateAPIView): pass


class UserDetail(UserMixin, generics.RetrieveUpdateDestroyAPIView): pass


class OrganizationMixin:
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (IsAuthenticated,)


class OrganizationList(OrganizationMixin, generics.ListCreateAPIView): pass


class OrganizationDetail(OrganizationMixin, generics.RetrieveDestroyAPIView): pass


class UserProfileManager(generics.ListCreateAPIView):
    def post(self, request):
        current_user = request.user
        data = json.loads(request.body)
        queryset = Profile.objects.get(user_id=current_user.id)
        queryset.bio = data['bio']
        queryset.ktp_no = data['ktp_no']
        queryset.npwp_no = data['npwp_no']
        queryset.phone_no = data['phone_no']
        queryset.birth_date = data['birth_date']
        queryset.save()
        return Response("Valid")

    def get(self, request):
        current_user = request.user
        data = json.loads(request.body)
        queryset = Profile.objects.get(user_id=current_user.id)
        serializer = UserProfileSerializer(queryset)
        return Response(serializer.data)


class NotificationManager(APIView):
    def get(self, request):
        queryset = Notification.objects.all()
        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        current_user = request.user
        profile = Profile.objects.get(user_id=current_user.id)
        access = AdministratorAccess.objects.get(id=current_user.id)
        json_data = json.loads(request.body)
        notification = Notification(title=json_data['title'])
        notification.access = access
        notification.save()
        unf = UserNotificationFeed()
        unf.user = profile
        unf.notification = notification
        unf.save()
        for component_id in json_data['components']:
            ucnr = UserComponentNotificationResponse(component_id=component_id)
            ucnr.profile = profile
            ucnr.notification = notification
            ucnr.save()
        return Response("Valid")


class NotificationDetail(APIView):
    def get(self, request, pk):
        notification = Notification.objects.get(id=pk)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)


class ComponentManager(APIView):
    def post(self, request):
        current_user = request.user
        profile = Profile.objects.get(user_id=current_user.id)
        json_data = json.loads(request.body)
        component = Component(title=json_data['title'], singleuse=json_data['singleuse'],
                              description=json_data['description'])
        component.profile = profile
        component.save()
        form = Form(value=json_data['form'])
        form.component = component
        form.save()
        return Response("Valid")

    def get(self, request):
        queryset = Component.objects.all()
        serializer = ComponentSerializer(queryset, many=True)
        return Response(serializer.data)


class ComponentDetail(APIView):
    def get(self, request, pk):
        component = Component.objects.get(id=pk)
        serializer = ComponentSerializer(component)
        return Response(serializer.data)


class UserNotificationManager(APIView):
    def get(self, request):
        current_user = request.user
        notifications = Notification.objects.filter(profile__user_id=current_user.id)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class UserNotificationDetail(APIView):
    def get(self, request, pk):
        current_user = request.user
        notifications = Notification.objects.filter(profile__user_id=current_user.id, id=pk)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class UserResponseManager(APIView):
    def post(self, request, pk):
        current_user = request.user
        json_data = json.loads(request.body)
        ucnr = UserComponentNotificationResponse.objects.get(profile=current_user.id, component=pk,
                                                             notification=json_data['id_notification'])
        print(json_data['value'])
        response = SimpleResponse(value=json_data['value'])
        response.save()
        ucnr.response = response
        ucnr.save()
        return Response("valid")


class testApi(APIView):
    def post(self, request):
        current_user = request.user
        profile = Profile.objects.get(user_id=current_user.id)
        access = AdministratorAccess.objects.get(id=current_user.id)
        json_data = json.loads(request.body)
        notification = Notification(title=json_data['title'])
        notification.access = access
        notification.save()
        unf = UserNotificationFeed()
        unf.user = profile
        unf.notification = notification
        unf.save()
        for component_id in json_data['components']:
            ucnr = UserComponentNotificationResponse(component_id=component_id)
            ucnr.profile = profile
            ucnr.notification = notification
            ucnr.save()
        return Response("Valid")

    def get(self, request):
        current_user = request.user
        queryset = Component.objects.filter(profile_id=current_user.id, singleuse=False)
        serializer = ComponentSerializer(queryset, many=True)
        return Response(serializer.data)
