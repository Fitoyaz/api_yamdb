from django_filters.filters import CharFilter
from rest_framework import serializers, validators
from rest_framework.fields import CharField, ReadOnlyField
from .models import User


class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role')
        model = User


class MeSerializer(serializers.ModelSerializer):
    role = ReadOnlyField()
    
    class Meta:
        fields = ('first_name', 'last_name', 'username', 'bio', 'email', 'role')
        model = User
        