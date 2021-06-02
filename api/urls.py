from django.urls import include
from django.urls import path

from rest_framework.routers import DefaultRouter

# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.views import TokenRefreshView

from api.views import CategoriesViewSet
from api.views import GenresViewSet
from api.views import TitlesViewSet

router = DefaultRouter()
router.register('categories', CategoriesViewSet, basename='category')
# router.register(
#     r'posts/(?P<id>[0-9]+)/comments',
#     CommentViewSet,
#     basename='comment_s'
# )
router.register('genres', GenresViewSet, basename='genre')
router.register('titles', TitlesViewSet, basename='title')

urlpatterns = [
    path('', include(router.urls)),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
