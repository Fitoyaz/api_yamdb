from rest_framework import serializers

from .models import Review, Comment


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


