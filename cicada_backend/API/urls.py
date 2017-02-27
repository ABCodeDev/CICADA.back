from django.conf.urls import url,include
from django.contrib import admin
from cicada_backend.API.views import *

urlpatterns = [
    url(r'^user-profile/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
    url(r'^user-profile/$', UserList.as_view()),
    url(r'^notification/$',NotificationList.as_view()),
    url(r'^notification/(?P<pk>[0-9]+)/$',NotificationDetail.as_view()),
    url(r'^organization/$', OrganizationList.as_view()),
    url(r'^organization/(?P<pk>[0-9]+)/$', OrganizationDetail.as_view())
]