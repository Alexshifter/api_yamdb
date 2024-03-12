from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt import serializers as token_serializers

from users.models import NewUser


class UserSerializer(serializers.ModelSerializer):

#    email = serializers.EmailField(max_length=254)
#    username = serializers.SlugField(max_length=150)

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

    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.SlugField(required=True, max_length=150)

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


class UserTokenSerializer(token_serializers.TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']
        self.fields['username'] = serializers.CharField()
        self.fields['confirmation_code'] = serializers.CharField()

    def validate(self, data):
        username = data['username']
        confirmation_code = data['confirmation_code']
        user = get_object_or_404(NewUser, username=username)
        if confirmation_code != user.confirmation_code:
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения.'}
            )
        refresh = self.get_token(user)
        token_string_access = str(refresh.access_token)
        return {'token': token_string_access}