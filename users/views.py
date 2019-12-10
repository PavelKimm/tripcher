from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from users.serializers import UserSerializer, GroupSerializer
from . import serializers
from .models import Profile
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from requests.exceptions import HTTPError
from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
from django.contrib.auth import login

from rest_framework_jwt.settings import api_settings

# jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
# jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly, )


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all().order_by('-id')
    serializer_class = serializers.ProfileSerializer


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = (IsOwnerOrReadOnly, )


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


# class SocialLoginView(generics.GenericAPIView):
#     """Log in using facebook"""
#     serializer_class = serializers.SocialSerializer
#     permission_classes = [permissions.AllowAny]
#
#     def post(self, request):
#         """Authenticate user through the provider and access_token"""
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         provider = serializer.data.get('provider', None)
#         strategy = load_strategy(request)
#
#         try:
#             backend = load_backend(strategy=strategy, name=provider,
#                                    redirect_uri=None)
#
#         except MissingBackend:
#             return Response({'error': 'Please provide a valid provider'},
#                             status=status.HTTP_400_BAD_REQUEST)
#         try:
#             if isinstance(backend, BaseOAuth2):
#                 access_token = serializer.data.get('access_token')
#             user = backend.do_auth(access_token)
#         except HTTPError as error:
#             return Response({
#                 "error": {
#                     "access_token": "Invalid token",
#                     "details": str(error)
#                 }
#             }, status=status.HTTP_400_BAD_REQUEST)
#         except AuthTokenError as error:
#             return Response({
#                 "error": "Invalid credentials",
#                 "details": str(error)
#             }, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             authenticated_user = backend.do_auth(access_token, user=user)
#
#         except HTTPError as error:
#             return Response({
#                 "error": "invalid token",
#                 "details": str(error)
#             }, status=status.HTTP_400_BAD_REQUEST)
#
#         except AuthForbidden as error:
#             return Response({
#                 "error": "invalid token",
#                 "details": str(error)
#             }, status=status.HTTP_400_BAD_REQUEST)
#
#         if authenticated_user and authenticated_user.is_active:
#             # generate JWT token
#             login(request, authenticated_user)
#             data = {
#                 "token": jwt_encode_handler(jwt_payload_handler(user))
#             }
#             # customize the response to your needs
#             response = {
#                 "email": authenticated_user.email,
#                 "username": authenticated_user.username,
#                 "token": data.get('token')
#             }
#             return Response(status=status.HTTP_200_OK, data=response)
