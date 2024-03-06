from django.shortcuts import render
from rest_framework import viewsets
from users.models import RequiredUser
from rest_framework import serializers
from users.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class UserViewSet(viewsets.ModelViewSet):

    model = RequiredUser
    queryset = RequiredUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = "username"
