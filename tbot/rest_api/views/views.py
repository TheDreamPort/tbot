from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from rest_api.serializers import UserSerializer
from knox.views import LoginView as KnoxLoginView

class UserAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = [BasicAuthentication]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)

