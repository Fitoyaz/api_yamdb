import router as router
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import UserViewSet, return_token, send_code, MeDetail
from rest_framework.routers import Route, SimpleRouter
from .views import (
    ReviewCommentDetailViewSet,
    ReviewDetailViewSet,
)

router_v1 = DefaultRouter()

# router_v1.register('users/me', MeViewSet, basename='MeApi')
router_v1.register('users', UserViewSet, basename='UsersApi')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewDetailViewSet, basename='review')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/('
                   r'?P<review_id>\d+)/comments',
                   ReviewCommentDetailViewSet, basename="reviews_comments")

urlpatterns = [

    path('v1/users/me/', MeDetail, name='send_code'),
    path('v1/auth/email/', send_code, name='send_code'),
    path('v1/auth/token/', return_token, name='send_token'),
    path('v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(
        'v1/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path('v1/', include(router_v1.urls)),
]


class CustomReadOnlyRouter(DefaultRouter):
    routes = [
        Route(
            url=r'^{prefix}$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
    ]
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
