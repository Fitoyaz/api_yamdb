from django.db.models import Avg
from rest_framework import serializers, validators
from rest_framework.fields import CharField, EmailField, ReadOnlyField

from api.models import Category, Comment, Genre, Review, Title, User


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
        

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class BaseTitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        if obj.reviews.exists():
            return obj.reviews.aggregate(rating=Avg('score')).get('rating')
        return None

    class Meta:
        fields = '__all__'
        model = Title


class TitlesCreateSerializer(BaseTitleSerializer):
    rating = serializers.SerializerMethodField(read_only=True)
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        many=False,
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')

    def get_rating(self, title):
        scores = Review.objects.filter(
            title_id=title.id).aggregate(Avg('score'))

        if scores:
            return scores['score__avg']
        return None


class TitlesReadSerializer(BaseTitleSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenresSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',
                  'rating')
