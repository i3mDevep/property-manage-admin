from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework import viewsets

from .serializers import MyTokenObtainPairSerializer, MyTokenRefreshSerializer, RegisterSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Login with username and password
    """
    serializer_class = MyTokenObtainPairSerializer

class MyTokenRefreshView(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    serializer_class = MyTokenRefreshSerializer

class RegisterUserView(viewsets.ModelViewSet):
    """
    Register new users with role coproperty and property
    """
    serializer_class = RegisterSerializer

