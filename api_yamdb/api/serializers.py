from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title
from reviews.constants import (
    MAX_VALUE_SCORE, MAX_LENGHT_NAME, MAX_LENGHT_SLUG, MIN_VALUE_SCORE
)


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=MAX_LENGHT_NAME,
        validators=[UniqueValidator(queryset=Category.objects.all())],
    )
    slug = serializers.SlugField(
        max_length=MAX_LENGHT_SLUG,
        validators=[UniqueValidator(queryset=Category.objects.all())],
    )

    class Meta:
        model = Category
        fields = ('name', 'slug')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    score = serializers.IntegerField(
        min_value=MIN_VALUE_SCORE,
        max_value=MAX_VALUE_SCORE
    )

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'author', 'score', 'pub_date'
        )

    def validate(self, data):
        request = self.context.get('request')
        title = get_object_or_404(
            Title,
            id=self.context.get('view').kwargs.get('title_id')
        )
        if request.method == 'POST':
            if title.reviews.filter(author=request.user):
                raise ValidationError(
                    ('На одно произведение '
                     'пользователь может оставить только один отзыв.')
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class GetTitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class PostPatchTitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    year = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True, max_length=MAX_LENGHT_NAME)

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Title
