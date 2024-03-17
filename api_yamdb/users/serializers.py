from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.tokens import RefreshToken

from users.constants import (MAX_LEN_EMAIL_FIELD,
                             MAX_LEN_USERNAME_FIELD)
from users.models import NewUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        model = NewUser
        validators = [
            UniqueTogetherValidator(
                queryset=NewUser.objects.all(),
                fields=('username', 'email',)
            )
        ]


class UserRegSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True,
                                   max_length=MAX_LEN_EMAIL_FIELD)
    username = serializers.SlugField(required=True,
                                     max_length=MAX_LEN_USERNAME_FIELD)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                f'Имя {value} не разрешено. Выберите другое имя.'
            )
        return value

    def validate(self, data):
        queryset = NewUser.objects.values_list('username', 'email')
        if queryset.filter(username=data['username']):
            raise serializers.ValidationError(
                {
                    'username': ('Пользователь с таким именем уже '
                                 'зарегистрирован. Выберите другое имя.')
                }
            )
        if queryset.filter(email=data['email']):
            raise serializers.ValidationError(
                {
                    'email': ('Пользователь с такой электронной '
                              'почтой уже зарегистрирован.')
                }
            )
        return data

    class Meta:
        model = NewUser
        fields = ('username', 'email',)


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(NewUser, username=username)
        if confirmation_code != default_token_generator.check_token(
            user,
            confirmation_code
        ):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения.'}
            )
        ref_token = RefreshToken(user)
        token_string_access = str(ref_token.access_token)
        return {'token': token_string_access}
