from django.urls import path, include
from rest_framework import routers

from .views import (PostList, PostDetail, PostCreation,
                    CommentViewSet)

router = routers.DefaultRouter()
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('posts/', PostList.as_view(), name='posts-list'),
    path('posts/new/', PostCreation.as_view(), name='post-creation'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('posts/<int:pk>/add_comment/', CommentViewSet.as_view({'post': 'create'}), name='add-comment'),
    path('posts/<int:pk>/delete_comment/', CommentViewSet.as_view({'delete': 'destroy'}), name='delete-comment'),
    path('posts/<int:pk>/edit_comment/', CommentViewSet.as_view({'put': 'update'}), name='edit-comment'),

    path('', include(router.urls))
]
# get pk for current post and implement choice of the post
