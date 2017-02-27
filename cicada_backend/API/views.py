from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import generics
from cicada_backend.models import *
from cicada_backend.API.serializers import *
from rest_framework.permissions import AllowAny

class UserMixin :
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (AllowAny,)

class UserList(UserMixin, generics.ListCreateAPIView): pass

class UserDetail(UserMixin, generics.RetrieveUpdateDestroyAPIView) : pass

class NotificationMixin :
    queryset = Notification.objects.all()
    serializers_class = NotificationSerializer
    permissions_classes = (AllowAny,)

class NotificationList(NotificationMixin, generics.ListCreateAPIView): pass

class NotificationDetail(NotificationMixin, generics.RetrieveDestroyAPIView) : pass


class OrganizationMixin:
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (AllowAny,)

class OrganizationList(OrganizationMixin, generics.ListCreateAPIView): pass

class OrganizationDetail(OrganizationMixin, generics.RetrieveDestroyAPIView) : pass