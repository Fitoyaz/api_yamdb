
from django_filters.filters import CharFilter
from rest_framework import serializers, validators
from rest_framework.fields import CharField, ReadOnlyField
from .models import User, Review, Comment


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

