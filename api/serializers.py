
from django_filters.filters import CharFilter
from rest_framework import serializers, validators
from rest_framework.fields import CharField, EmailField, ReadOnlyField

from api.models import Categories, Genres, Titles

from .models import Comment, Review, User


class UserSerializer(serializers.ModelSerializer):
    username = CharField(
        max_length=20,
        validators=[validators.UniqueValidator(queryset=User.objects.all())],
        required=True
    )
    email = EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
        model = User
        lookup_field = 'username'


class MeSerializer(serializers.ModelSerializer):
    role = ReadOnlyField()

    class Meta:
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
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
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitlesSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset = Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        many=False,
        slug_field='slug',
        queryset = Categories.objects.all()
    )
    
    # author = serializers.ReadOnlyField(source='author.username')
    # user = serializers.SlugRelatedField(
    #     slug_field='username',
    #     read_only=True,
    #     default=serializers.CurrentUserDefault()
    # )
    # following = serializers.SlugRelatedField(
    #     slug_field='username',
    #     queryset=User.objects.all())

    class Meta:
        model = Titles
        fields = ('__all__')
