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


class UserProfileManager(APIView):
    def post(self, request):
        current_user = request.user
        data = json.loads(request.body)
        user = User.objects.get(id=current_user.id)
        profile = Profile(user=user)
        profile.bio = data['bio']
        profile.ktp_no = data['ktp_no']
        profile.npwp_no = data['npwp_no']
        profile.phone_no = data['phone_no']
        profile.birth_date = data['birth_date']
        profile.save()


    def patch(self, request):
        current_user = request.user
        data = json.loads(request.body)
        profile = Profile.objects.get(user_id=current_user.id)
        profile.bio = data['bio']
        profile.ktp_no = data['ktp_no']
        profile.npwp_no = data['npwp_no']
        profile.phone_no = data['phone_no']
        profile.birth_date = data['birth_date']
        profile.save()
        return Response(profile.id)

    def get(self, request):
        current_user = request.user
        queryset = Profile.objects.get(user_id=current_user.id)
        serializer = UserProfileSerializer(queryset)
        return Response(serializer.data)


class NotificationManager(APIView):
    def get(self, request):
        queryset = Notification.objects.all()
        serializer = NotificationComponentSerializer(queryset, many=True)
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
        serializer = NotificationComponentSerializer(notification)
        return Response(serializer.data)


class ComponentManager(APIView):
    def post(self, request):
        current_user = request.user
        profile = Profile.objects.get(user_id=current_user.id)
        json_data = json.loads(request.body)
        component = Component(title=json_data['title'], single_use=json_data['single_use'],
                              description=json_data['description'], type=json_data['type'])
        component.profile = profile
        component.save()
        form = Form(value=json_data['form'])
        form.component = component
        form.save()
        return Response("Valid")

    def get(self, request):
        queryset = Component.objects.all()
        serializer = ComponentSerializer(queryset, many=True)
        # serializer_data = []
        # for e in queryset:
        #     e_serializer = ComponentSerializer(e)
        #     dict = e_serializer.data
        #     if e.type == 'form':
        #         form = Form.objects.get(component=e)
        #         form_serializer = FormSerializer(form)
        #         dict['data'] = form_serializer.data
        #     serializer_data.append(dict)
        return Response(serializer.data)


class ComponentDetail(APIView):
    def get(self, request, pk):
        component = Component.objects.get(id=pk)
        serializer = ComponentSerializer(component)
        serializer_dict = serializer.data
        if component.type == 'form':
            form = Form.objects.get(component=component)
            form_serializer = FormSerializer(form)
            serializer_dict['data'] = form_serializer.data
        return Response(serializer_dict)


class UserNotificationManager(APIView):
    def get(self, request):
        current_user = request.user
        notifications = Notification.objects.filter(profile__user_id=current_user.id)
        serializer = NotificationComponentSerializer(notifications, many=True)
        return Response(serializer.data)


class UserNotificationDetail(APIView):
    def get(self, request, pk):
        current_user = request.user
        notification = Notification.objects.get(profile__user_id=current_user.id, id=pk)
        notification_dict = NotificationSerializer(notification).data
        notification_dict['components_id'] = notification_dict.pop('components')
        notification_dict['component'] = []
        for component_id in notification_dict['components_id']:
            component = Component.objects.get(id=component_id)
            component_dict = ComponentSerializer(component).data
            if component.type == 'form':
                form = Form.objects.get(component=component)
                form_serializer = FormSerializer(form)
                component_dict['data'] = form_serializer.data
            notification_dict['component'].append(component_dict)
        return Response(notification_dict)


class UserResponseManager(APIView):
    def post(self, request):
        current_user = request.user
        json_data = json.loads(request.body)
        ucnr = UserComponentNotificationResponse.objects.get(profile=current_user.id,
                                                             component__id=json_data['component_id'],
                                                             notification=json_data['notification_id'])
        print(json_data['value'])
        response = SimpleResponse(value=json_data['value'])
        response.save()
        ucnr.response = response
        ucnr.save()
        return Response(response.id)
