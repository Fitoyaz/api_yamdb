from django.contrib.auth import get_user_model

from rest_framework import serializers

from api.models import Categories
from api.models import Genres
from api.models import Titles

User = get_user_model()


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('__all__')


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('__all__')


class TitlesSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all())

    class Meta:
        model = Titles
        fields = ('__all__')
