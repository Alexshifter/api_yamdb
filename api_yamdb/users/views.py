from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import (decorators, filters, mixins, pagination, status,
                            viewsets)
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
    pagination_class = pagination.LimitOffsetPagination
    lookup_field = 'username'
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
        serializer.save(role=current_user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegView(mixins.CreateModelMixin, viewsets.GenericViewSet):

    queryset = NewUser.objects.all()
    serializer_class = UserRegSerializer
    model = NewUser

    def get_code_and_send_mail_to_user(self, user):

        confirmation_code = default_token_generator.make_token(user)

        return send_mail(
            subject='Your confirmation code on YAMDB',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

    def create(self, request):
        rq_data = request.data
        try:
            exist_user = NewUser.objects.get(
                username=rq_data.get('username'),
                email=rq_data.get('email')
            )
            self.get_code_and_send_mail_to_user(exist_user)
            return Response(rq_data, status=status.HTTP_200_OK)

        except NewUser.DoesNotExist:
            serializer = self.get_serializer(data=rq_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            exist_user = NewUser.objects.get(
                username=serializer.data.get('username'),
                email=serializer.data.get('email')
            )
            self.get_code_and_send_mail_to_user(exist_user)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)


class UserTokenView(TokenObtainPairView):

    serializer_class = UserTokenSerializer
