
from django_filters.filters import CharFilter
from rest_framework import serializers, validators
from rest_framework.fields import CharField, ReadOnlyField
from .models import User, Review, Comment
from api.models import Categories
from api.models import Genres
from api.models import Titles


class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role')
        model = User


class MeSerializer(serializers.ModelSerializer):
    role = ReadOnlyField()
    
    class Meta:
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role')
        model = User


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title = serializers.ReadOnlyField(source='post_id')

    class Meta:
        fields = '__all__'
        model = Review


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title = serializers.ReadOnlyField(source='post_id')

    class Meta:
        fields = '__all__'
        model = Comment


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
