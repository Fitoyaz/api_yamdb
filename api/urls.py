from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ReviewCommentDetailViewSet,
    ReviewDetailViewSet,
)

router = DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewDetailViewSet, basename='review')
router.register(r'titles/(?P<title_id>\d+)/reviews/('
                r'?P<review_id>\d+)/comments',
                ReviewCommentDetailViewSet, basename="reviews_comments")

urlpatterns = [
    path('v1/', include(router.urls))
]
