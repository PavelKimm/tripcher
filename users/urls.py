from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import UserCreateView, UserViewSet, GroupViewSet, \
                   ProfileCreateView, ProfileListView, ProfileDetailView
from rest_framework.authtoken import views
from django.contrib.auth.views import LoginView


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('profiles/', ProfileListView.as_view(), name=''),
    path('profiles/create', ProfileCreateView.as_view(), name=''),
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('registration/', UserCreateView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),

]

# # Default login/logout views
# urlpatterns += [
#     path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
# ]

