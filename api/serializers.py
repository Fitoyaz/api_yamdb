from django.db.models import Avg

from rest_framework import serializers
from rest_framework import validators

from rest_framework.fields import CharField
from rest_framework.fields import EmailField
from rest_framework.fields import ReadOnlyField

from api.models import Categories
from api.models import Comment
from api.models import Genres
from api.models import Review
from api.models import Titles
from api.models import User


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
    title = serializers.SlugRelatedField(
        slug_field='id', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.SlugRelatedField(
        slug_field='id', read_only=True)

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


class TitlesReadSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(many=True, read_only=True)
    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class TitlesCreateSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(read_only=True)
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        many=False,
        slug_field='slug',
        queryset=Categories.objects.all()
    )

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')

    def get_rating(self, titles):
        scores = Review.objects.filter(
            titles_id=titles.id).aggregate(Avg('score'))
        if scores:
            return scores['score__avg']
        return None

# author = serializers.ReadOnlyField(source='author.username')
    # user = serializers.SlugRelatedField(
    #     slug_field='username',
    #     read_only=True,
    #     default=serializers.CurrentUserDefault()
    # )
    # following = serializers.SlugRelatedField(
    #     slug_field='username',
    #     queryset=User.objects.all())
