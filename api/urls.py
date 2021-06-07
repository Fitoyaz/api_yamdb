from django.urls import include, path
from rest_framework.routers import DefaultRouter, Route
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api.views import (CategoriesViewSet, GenreDelViewSet,
                       GenresViewSet, TitlesViewSet)

from .views import (MeDetail, ReviewCommentDetailViewSet, ReviewDetailViewSet,
                    UserViewSet, return_token, send_code)

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='UsersApi')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewDetailViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/('
                   r'?P<review_id>\d+)/comments',
                   ReviewCommentDetailViewSet, basename="reviews_comments")
router_v1.register('categories', CategoriesViewSet, basename='category')
# router_v1.register(
#     'categories/<slug:slug>/',
#     CategoryDelViewSet,
#     basename='del_cat'
#)
router_v1.register('genres', GenresViewSet, basename='genre')
router_v1.register(
    'genres/<slug:slug>/',
    GenreDelViewSet,
    basename='del_genre'
)
router_v1.register('titles', TitlesViewSet, basename='title')
# router_v1.register(
#     r'titles/(?P<id>[0-9]+)/',
#     TitleViewSet,
#     basename='comment_s'
# )


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
