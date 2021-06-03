from django.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter

from api.views import CategoriesViewSet
from api.views import CategoryDelViewSet
from api.views import GenresViewSet
from api.views import GenreDelViewSet
from api.views import TitleViewSet
from api.views import TitlesViewSet

router = DefaultRouter()
router.register('categories', CategoriesViewSet, basename='category')
router.register(
    'categories/<slug:slug>/',
    CategoryDelViewSet,
    basename='del_cat'
)
router.register('genres', GenresViewSet, basename='genre')
router.register('genres/<slug:slug>/', GenreDelViewSet, basename='del_genre')
router.register('titles', TitlesViewSet, basename='title')
router.register(r'titles/(?P<id>[0-9]+)', TitleViewSet, basename='comment_s')

urlpatterns = [
    path('', include(router.urls)),
]
