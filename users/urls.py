from django.urls import path, include
from rest_framework import routers
from .views import (UserCreateView, UserViewSet, GroupViewSet,
                    ProfileListView, ProfileDetailView,
                    # SocialLoginView
                    )


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('create_user/', UserCreateView.as_view(), name='user-create'),
    path('profiles/', ProfileListView.as_view(), name='profiles-list'),
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('', include(router.urls)),
    path('', include('django.contrib.auth.urls')),
    path('base-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include('rest_framework_social_oauth2.urls')),

    path('', include('social_django.urls')),
    # http://localhost:8000/api/v1/login/vk-oauth2 --- authentication

    # path('rest-auth/', include('rest_auth.urls')),
]
