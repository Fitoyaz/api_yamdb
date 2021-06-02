# from django.shortcuts import render
from django.contrib.auth import get_user_model

# from django.shortcuts import get_object_or_404

# from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
# from rest_framework import permissions

# from rest_framework.permissions import IsAuthenticated

from api.models import Categories
from api.models import Genres
from api.models import Titles

# from api.permissions import IsAuthorOrReadOnlyPermission

from api.serializers import CategoriesSerializer
from api.serializers import GenresSerializer
from api.serializers import TitlesSerializer

User = get_user_model()


class GetPostDelModelViewSet(mixins.CreateModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.DestroyModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `destroy()` and
    `list()` actions.
    """
    pass


class CategoriesViewSet(GetPostDelModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pass


class GenresViewSet(GetPostDelModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pass


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    pass


# class PostViewSet(viewsets.ModelViewSet):
    # serializer_class = PostSerializer
    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly,
    #     IsAuthorOrReadOnlyPermission
    # ]

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

    # def get_queryset(self):
    #     queryset = Post.objects.all()
    #     group_name = self.request.query_params.get('group', None)
    #     if group_name is not None:
    #         queryset = queryset.filter(group=group_name)
    #     return queryset


# class GroupViewSet(GetPostModelViewSet):
    # queryset = Group.objects.all()
    # serializer_class = GroupSerializer
    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly,
    #     IsAuthorOrReadOnlyPermission
    # ]


# class CommentViewSet(viewsets.ModelViewSet):
    # serializer_class = CommentSerializer
    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly,
    #     IsAuthorOrReadOnlyPermission
    # ]

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

    # def get_queryset(self):
    #     post = get_object_or_404(Post, id=self.kwargs['id'])
    #     queryset = post.comments.all()
    #     return queryset


# class FollowViewSet(GetPostModelViewSet):
#     serializer_class = FollowSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.SearchFilter]
#     search_fields = ('user__username',)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     def get_queryset(self):
#         queryset = Follow.objects.filter(following=self.request.user)
#         return queryset
