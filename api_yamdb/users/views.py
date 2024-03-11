<<<<<<< HEAD
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
    lookup_field = 'username'
=======
import random

from django.core.mail import send_mail
from rest_framework import decorators, filters, mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import NewUser
from users.permissions import IsAdminOnly
from users.serializers import (UserRegSerializer, UserSerializer,
                               UserTokenSerializer)


class UserViewSet(viewsets.ModelViewSet):
    model = NewUser
    queryset = NewUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOnly,)
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @decorators.action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        current_user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(current_user)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        serializer = self.get_serializer(
            instance=current_user,
            data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegView(mixins.CreateModelMixin, viewsets.GenericViewSet):

    queryset = NewUser.objects.all()
    serializer_class = UserRegSerializer
    model = NewUser

    def send_mail_to_user(self, confirmation_code, email):
        return send_mail(
            subject='Your confirmation code on YAMDB',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email='admin@yamdb.not',
            recipient_list=[email],
        )

    def get_exist_user(self, username):
        return NewUser.objects.get(username=username)

    def create(self, request):
        confirmation_code = random.randint(100, 999)
        try:
            exist_user = NewUser.objects.get(
                username=request.data.get('username'),
                email=self.request.data.get('email')
            )

            exist_user.confirmation_code = confirmation_code
            exist_user.save()
            self.send_mail_to_user(confirmation_code, exist_user.email)
            return Response(request.data, status=status.HTTP_200_OK)

        except NewUser.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(confirmation_code=confirmation_code)
            self.send_mail_to_user(confirmation_code,
                                   serializer.data.get('email'))
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data,
                            status=status.HTTP_200_OK,
                            headers=headers)


class UserTokenView(TokenObtainPairView):

    serializer_class = UserTokenSerializer
>>>>>>> feature/reg_auth_users
