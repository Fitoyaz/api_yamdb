from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.models import Categories, Genres, Titles
from api.permissions import IsAdminOrReadOnly, IsAdminRole, \
    IsStaffOrOwnerOrReadOnly
from api.serializers import (CategoriesSerializer, GenresSerializer,
                             TitlesSerializer)

from api.auth_functions import generate_random_string, get_tokens_for_user
from api.models import ConfCode, Review, User

from api.serializers import (CommentsSerializer, MeSerializer,
                             ReviewsSerializer, UserSerializer)
from django_filters.rest_framework import DjangoFilterBackend


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
                ucc = ConfCode(
                    email=newmail,
                    eml_conf_code=eml_conf_code,
                    user=user
                )
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
    permission_classes = [IsAdminRole]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'    


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


class ReviewDetailViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [IsStaffOrOwnerOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class ReviewCommentDetailViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [IsStaffOrOwnerOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'),
                                   title=self.kwargs.get('title_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'),
                                   title=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)


# class CategoriesViewSet(viewsets.ModelViewSet):
class CategoriesViewSet(mixins.CreateModelMixin,  # POST-запросы
                        mixins.RetrieveModelMixin,  # GET-запросы
                        mixins.ListModelMixin,  # только для чтения
                        viewsets.GenericViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', 'slug')


# class CategoryDelViewSet(viewsets.ModelViewSet):
class CategoryDelViewSet(mixins.DestroyModelMixin,  # DELETE-запросы
                         viewsets.GenericViewSet):
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminRole, ]

    def get_queryset(self):
        queryset = get_object_or_404(Categories, id=self.kwargs['id'])
        return queryset


# class GenresViewSet(viewsets.ModelViewSet):
class GenresViewSet(mixins.CreateModelMixin,  # POST-запросы
                    mixins.RetrieveModelMixin,  # GET-запросы
                    mixins.ListModelMixin,  # только для чтения
                    viewsets.GenericViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', 'slug')


# class GenreDelViewSet(viewsets.ModelViewSet):
class GenreDelViewSet(mixins.DestroyModelMixin,  # DELETE-запросы
                      viewsets.GenericViewSet):
    serializer_class = GenresSerializer
    permission_classes = [IsAdminRole, ]

    def get_queryset(self):
        queryset = get_object_or_404(Genres, id=self.kwargs['id'])
        return queryset


# class TitlesViewSet(viewsets.ModelViewSet):
class TitlesViewSet(mixins.CreateModelMixin,  # POST-запросы
                    mixins.RetrieveModelMixin,  # GET-запросы
                    mixins.ListModelMixin,  # только для чтения
                    viewsets.GenericViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', 'year', 'category__slug', 'genre__slug')


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
