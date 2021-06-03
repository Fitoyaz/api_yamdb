from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, mixins, permissions, serializers, status,
                            viewsets)
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .auth_functions import generate_random_string, get_tokens_for_user
from .models import ConfCode, User
from .permissions import IsAdmin, IsModerator, IsOwnerOrReadOnly
from .serializers import UserSerializer


@api_view(['POST'])
def send_code(request):
    if 'email' in request.data:
        eml_conf_code = generate_random_string(3)
        newmail = request.data['email']
        if User.objects.filter(email=newmail).count() > 0:
            user = get_object_or_404(User, email=newmail)
            ucc = get_object_or_404(ConfCode, user=user)
            ucc.email = newmail
            ucc.eml_conf_code = eml_conf_code
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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', ]
