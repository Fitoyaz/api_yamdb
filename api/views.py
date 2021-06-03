from django.contrib.auth import get_user_model

from django.shortcuts import get_object_or_404

from rest_framework import mixins
from rest_framework import viewsets

from api.models import Categories
from api.models import Genres
from api.models import Titles

from api.permissions import IsAdmin
from api.permissions import IsAdminOrReadOnly

from api.serializers import CategoriesSerializer
from api.serializers import GenresSerializer
from api.serializers import TitlesSerializer

User = get_user_model()


class CategoriesViewSet(mixins.CreateModelMixin,  # POST-запросы
                        mixins.RetrieveModelMixin,  # GET-запросы
                        mixins.ListModelMixin,  # только для чтения
                        viewsets.GenericViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class CategoryDelViewSet(mixins.DestroyModelMixin,  # DELETE-запросы
                         viewsets.GenericViewSet):
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdmin, ]

    def get_queryset(self):
        queryset = get_object_or_404(Categories, id=self.kwargs['id'])
        return queryset


class GenresViewSet(mixins.CreateModelMixin,  # POST-запросы
                    mixins.RetrieveModelMixin,  # GET-запросы
                    mixins.ListModelMixin,  # только для чтения
                    viewsets.GenericViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class GenreDelViewSet(mixins.DestroyModelMixin,  # DELETE-запросы
                      viewsets.GenericViewSet):
    serializer_class = GenresSerializer
    permission_classes = [IsAdmin, ]

    def get_queryset(self):
        queryset = get_object_or_404(Genres, id=self.kwargs['id'])
        return queryset


class TitlesViewSet(mixins.CreateModelMixin,  # POST-запросы
                    mixins.RetrieveModelMixin,  # GET-запросы
                    mixins.ListModelMixin,  # только для чтения
                    viewsets.GenericViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class TitleViewSet(mixins.RetrieveModelMixin,  # GET-запросы
                   mixins.UpdateModelMixin,  # PATCH-запросы
                   mixins.DestroyModelMixin,  # DELETE-запросы
                   mixins.ListModelMixin,  # только для чтения
                   viewsets.GenericViewSet):
    serializer_class = TitlesSerializer
    permission_classes = [IsAdminOrReadOnly, ]

    def get_queryset(self):
        queryset = get_object_or_404(Titles, id=self.kwargs['id'])
        return queryset
