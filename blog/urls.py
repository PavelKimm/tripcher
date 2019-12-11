from django.urls import path
from .views import (PostList, PostDetail, PostCreation)


urlpatterns = [
    path('posts/', PostList.as_view(), name='posts-list'),
    path('posts/new/', PostCreation.as_view(), name='post-creation'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),
]
