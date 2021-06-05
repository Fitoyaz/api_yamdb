from django.core.mail import send_mail
from django.http import request
from django.shortcuts import get_object_or_404
from rest_framework import (filters, mixins, permissions, serializers, status,
                            viewsets)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .auth_functions import generate_random_string, get_tokens_for_user
from .models import ConfCode, User
from .permissions import IsAdmin, IsModerator, IsOwnerOrReadOnly
from .serializers import MeSerializer, UserSerializer


@api_view(['POST'])
def send_code(request):
    if 'email' in request.data:
        eml_conf_code = generate_random_string(3)
        newmail = request.data['email']
        if User.objects.filter(email=newmail).count() > 0:
            user = get_object_or_404(User, email=newmail)
            if ConfCode.objects.filter(user=user).count() > 0:
                ucc = get_object_or_404(ConfCode, user=user)
                ucc.email = newmail
                ucc.eml_conf_code = eml_conf_code
                ucc.save()
            else:
                ucc = ConfCode(email=newmail, eml_conf_code=eml_conf_code, user=user)
                ucc.save()
        else:
            if ConfCode.objects.filter(email=newmail).count() == 0:
                ucc = ConfCode(email=newmail, eml_conf_code=eml_conf_code)
                ucc.save()
            else:
                ucc = ConfCode.objects.filter(email=newmail)[0]
                ucc.eml_conf_code = eml_conf_code
                ucc.save()

        send_mail(
            'confirmation',
            eml_conf_code,
            'from@example.com',
            [f'{newmail}'],
            fail_silently=False,
        )
        st = status.HTTP_200_OK
        response = {"email": newmail}
    else:
        st = status.HTTP_400_BAD_REQUEST
        response = request.data
    return Response(response, status=st)


@api_view(['POST'])
def return_token(request):
    if 'email' and 'confirmation_code' in request.data:
        email = request.data['email']
        eml_conf_code = request.data['confirmation_code']
        if ConfCode.objects.filter(email=email).count() > 0:
            ucc = ConfCode.objects.filter(email=email)[0]
            if ucc.eml_conf_code == eml_conf_code:
                if User.objects.filter(confcode=ucc).count() != 0:
                    user = get_object_or_404(User, confcode=ucc)
                else:
                    user = User.objects.create(username=email)
                    user.email = email
                    user.save()
                    ucc.user = user
                    ucc.save()
                token = get_tokens_for_user(user=user)
                response = {"token": token}
                st = status.HTTP_200_OK
            else:
                st = status.HTTP_204_NO_CONTENT
                response = {"message": "wrong conf code"}
        else:
            st = status.HTTP_404_NOT_FOUND
            response = {"message": "email not found"}
    else:
        st = status.HTTP_400_BAD_REQUEST
        response = request.data
    return Response(response, status=st)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    serializer_class = UserSerializer    
    filterset_fields = ['username', ]


@api_view(['PATCH', 'GET'])
@permission_classes([permissions.IsAuthenticated])
def MeDetail(request):
    user = request.user
    serializer = MeSerializer(user)
    if request.method == 'GET':
        serializer = MeSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'PATCH':
        serializer = MeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Review
from .permissions import ReviewOwnerPermission
from .serializers import (
    ReviewsSerializer,
    CommentsSerializer,
)


class ReviewDetailViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ReviewOwnerPermission]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class ReviewCommentDetailViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ReviewOwnerPermission]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'),
                                   title=self.kwargs.get('title_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'),
                                   title=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)
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
