from django.urls import path, include
from rest_auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from rest_framework import routers
from .views import (UserCreateView, UserListView, UserDetailView, GroupViewSet,
                    ProfileListView, ProfileDetailView,
                    CurrentUserProfileView, change_friend,
                    FriendsListView)


router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserListView.as_view(), name='users-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/signup/', UserCreateView.as_view(), name='user-create'),
    path('users/profile/', CurrentUserProfileView.as_view(), name='current-user-profile'),

    path('profiles/', ProfileListView.as_view(), name='profiles-list'),
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),

    path('base-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include('rest_framework_social_oauth2.urls')),
    path('', include('social_django.urls')),
    # http://localhost:8000/api/v1/login/vk-oauth2 --- authentication

    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(),
         name='rest_password_reset_confirm'),

    path('users/<str:operation>/<int:pk>/', change_friend, name='change_friend'),
    path('friends/', FriendsListView.as_view(), name='friends_list'),
]
