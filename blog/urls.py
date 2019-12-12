from django.urls import path, include
from rest_framework import routers

from .views import (PostList, PostDetail, CommentViewSet, DraftCreation, like)

router = routers.DefaultRouter()
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('posts/', PostList.as_view(), name='posts-list'),
    path('posts/create/', DraftCreation.as_view(), name='post-creation'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('posts/<int:pk>/like/', like, name='post-like'),

    path('', include(router.urls)),
    path('posts/<int:pk>/comments/', CommentViewSet.as_view({'get': 'list'}), name='comments-list'),
    path('posts/<int:pk>/comments/create/', CommentViewSet.as_view({'post': 'create'}), name='comment-add'),
    path('posts/<int:pk>/comments/delete/<int:comment_id>/',
         CommentViewSet.as_view({'delete': 'destroy'}), name='comment-delete'),
    path('posts/<int:pk>/comments/edit/<int:comment_id>/',
         CommentViewSet.as_view({'patch': 'partial_update'}), name='comment-edit'),
]
