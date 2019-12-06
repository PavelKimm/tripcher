from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import UserCreate, UserViewSet, GroupViewSet, ProfileViewSet
from rest_framework.authtoken import views
from django.contrib.auth.views import LoginView


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'profiles', ProfileViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('registration/', UserCreate.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth')
]

# # Default login/logout views
# urlpatterns += [
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
# ]

