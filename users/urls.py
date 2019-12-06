from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import UserList, UserDetail, \
    GroupList, GroupDetail, ProfileList, ProfileDetail, UserViewSet, GroupViewSet, ProfileViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'profiles', ProfileViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('groups/', GroupList.as_view(), name='group-list'),
    path('groups/<int:pk>/', GroupDetail.as_view(), name='group-detail'),
    path('profile/', ProfileList.as_view(), name='profile-list'),
    path('profiles/<int:pk>/', ProfileDetail.as_view(), name='profile-detail'),
    path('', include(router.urls)),
]

# Default login/logout views
urlpatterns += [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]


