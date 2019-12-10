from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from rest_framework.views import APIView

from . import serializers
from .models import Profile
from .permissions import IsOwnerOrReadOnly, IsCurrentUserOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from django.shortcuts import redirect


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsCurrentUserOrReadOnly, )


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = (IsOwnerOrReadOnly, )


class CurrentUserProfileView(APIView):
    def get(self, request):
        profile = self.request.user.profile
        serializer = serializers.ProfileSerializer(profile, context={'request': request})
        return Response({'profile': serializer.data})


class UserCreateView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


class FriendsListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.FriendsSerializer


def change_friend(request, operation, pk):
    to_profile = Profile.objects.get(pk=pk)
    if operation == 'add':
        Profile.make_friend(request.user, to_profile)
    elif operation == 'remove':
        Profile.remove_friend(request.user, to_profile)
    return redirect('current-user-profile')
