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
