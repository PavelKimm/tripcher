from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.shortcuts import redirect, get_object_or_404
from . import serializers
from .models import Profile
from .permissions import IsOwnerOrReadOnly, IsCurrentUserOrReadOnly


class UserCreateView(generics.CreateAPIView):
    serializer_class = serializers.UserCreationSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (IsCurrentUserOrReadOnly, )


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


class FriendsListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.FriendsSerializer


class ChangeFriend(APIView):
    def post(self, request, operation, pk):
        to_profile = get_object_or_404(Profile, pk=pk)
        if request.user.profile.id != pk:
            if operation == 'add':
                Profile.make_friend(request.user, to_profile)
            elif operation == 'remove':
                Profile.remove_friend(request.user, to_profile)
        return redirect('current-user-profile')
