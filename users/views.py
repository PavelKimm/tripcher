from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from users.serializers import UserSerializer, GroupSerializer
from .serializers import ProfileSerializer
from .models import Profile

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ProfileCreateView(generics.CreateAPIView):
    """
    API endpoint that allows profiles to be created.
    """
    serializer_class = ProfileSerializer


class ProfileListView(generics.ListAPIView):
    """
    API endpoint that allows all profiles to be viewed as list.
    """
    queryset = Profile.objects.all().order_by('-id')
    serializer_class = ProfileSerializer


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows profiles to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


