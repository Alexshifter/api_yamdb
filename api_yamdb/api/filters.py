from django_filters.rest_framework import CharFilter, FilterSet

from reviews.models import Title


class TitleFilterForGenreCategory(FilterSet):
    genre = CharFilter(field_name='genre__slug',)
    category = CharFilter(field_name='category__slug',)
    name = CharFilter(field_name='name')
    year = CharFilter(field_name='year')

    class Meta:
        fields = ('genre', 'category', 'name', 'year')
        model = Title
