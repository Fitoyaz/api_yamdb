import string

from django.core.mail import send_mail

from django.contrib.auth.tokens import default_token_generator

from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import get_object_or_404

from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters

from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes

from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from api.auth_functions import generate_random_string
from api.auth_functions import get_tokens_for_user

from api.mine_viewsets import ListCreateDestroyViewSet

from api.models import Categories, ConfCode, Review, User, Genres, Titles

from api.permissions import IsAdminOrReadOnly
from api.permissions import IsAdminRole
from api.permissions import IsStaffOrOwnerOrReadOnly

from api.serializers import CategoriesSerializer
from api.serializers import CommentsSerializer
from api.serializers import GenresSerializer
from api.serializers import MeSerializer
from api.serializers import ReviewsSerializer
from api.serializers import TitlesCreateSerializer
from api.serializers import TitlesReadSerializer
from api.serializers import UserSerializer


@api_view(['POST'])
def send_code(request):
    if not request.data.get('email'):        
        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
    newmail = request.data.get('email')
    user, created = User.objects.get_or_create(email=newmail, 
    defaults={'username': newmail, 'is_active': 0})
    confirmation_code = default_token_generator.make_token(user)    
    send_mail(
        'confirmation',
        confirmation_code,
        'from@example.com',
        [f'{newmail}'],
        fail_silently=False,
    )    
    return Response(request.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def return_token(request):
    if not 'email' and 'confirmation_code' in request.data:
        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
    email = request.data.get('email')
    confirmation_code = request.data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    if default_token_generator.check_token(user=user, token=confirmation_code):
        if user.is_active == False:
             user.is_activate = True
             cleaner = str.maketrans(dict.fromkeys(string.punctuation))        
             user.username = email.translate(cleaner)
             user.save()
        token = RefreshToken.for_user(user)
        response = {"token": str(token)}
        st = status.HTTP_200_OK
    else:
        st = status.HTTP_204_NO_CONTENT
        response = {"message": "wrong conf code"}
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


class CategoriesViewSet(ListCreateDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(ListCreateDestroyViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class GenreDelViewSet(mixins.DestroyModelMixin,  # DELETE-запросы
                      viewsets.GenericViewSet):
    serializer_class = GenresSerializer
    permission_classes = [IsAdminRole, ]

    def get_queryset(self):
        queryset = get_object_or_404(Genres, id=self.kwargs['id'])
        return queryset


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    # permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    # serializer_class = TitlesReadeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'year', 'category__slug', 'genre__slug']
    lookup_field = 'titles_id'
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == ('create' or 'partial_update'):
            return TitlesCreateSerializer
        return TitlesReadSerializer

# class TitlesViewSet(viewsets.ModelViewSet):
# class TitlesViewSet(mixins.CreateModelMixin,  # POST-запросы
#                     mixins.RetrieveModelMixin,  # GET-запросы
#                     mixins.ListModelMixin,  # только для чтения
#                     viewsets.GenericViewSet):
#     queryset = Titles.objects.all()
#     serializer_class = TitlesSerializer
#     permission_classes = [IsAdminOrReadOnly, ]
#     filter_backends = [filters.SearchFilter]
#     search_fields = ('name', 'year', 'category__slug', 'genre__slug')


# class TitleViewSet(mixins.RetrieveModelMixin,  # GET-запросы
#                    mixins.UpdateModelMixin,  # PATCH-запросы
#                    mixins.DestroyModelMixin,  # DELETE-запросы
#                    mixins.ListModelMixin,  # только для чтения
#                    viewsets.GenericViewSet):
#     serializer_class = TitlesSerializer
#     permission_classes = [IsAdminOrReadOnly, ]

#     def get_queryset(self):
#         queryset = get_object_or_404(Titles, id=self.kwargs['id'])
#         return queryset
