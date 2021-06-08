from django_filters import rest_framework as filters

from api.models import Titles

    
class TitleFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains' )
    year = filters.NumberFilter(field_name='year')
    genre = filters.CharFilter(field_name='genre__slug', lookup_expr='slug')
    category = filters.CharFilter(field_name='category__slug', lookup_expr='slug')

    class Meta:
        model = Titles
        fields = ['name', 'year', 'genre', 'category']
