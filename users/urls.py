from django.urls import path, include
from rest_framework import routers
# from rest_framework.authtoken import views
from .views import (UserCreateView, UserViewSet,
                    GroupViewSet, ProfileCreateView,
                    ProfileListView, ProfileDetailView,
                    SocialLoginView
                    )


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('', include(router.urls)),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),
    # http://localhost:8000/api/v1/login/vk-oauth2 --- authentication

    path('profiles/', ProfileListView.as_view(), name='profiles-list'),
    path('profiles/create', ProfileCreateView.as_view(), name='profile-create'),
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),

    # path('auth/', include('djoser.urls')),
    # path('auth_token/', include('djoser.urls.authtoken')),
    # path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path('base-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/', include('rest_framework_social_oauth2.urls')),
    path('oauth/login/', SocialLoginView.as_view()),

    path('rest-auth/', include('rest_auth.urls')),
]
