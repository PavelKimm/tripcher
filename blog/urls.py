from django.urls import path, include
from rest_framework import routers

from .views import (PostList, PostDetail, CommentViewSet, like,
                    DraftCreation, DraftList, DraftDetail,
                    confirm_draft)

router = routers.DefaultRouter()
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('posts/', PostList.as_view(), name='posts-list'),
    path('posts/create/', DraftCreation.as_view(), name='post-creation'),
    path('drafts/', DraftList.as_view(), name='drafts-list'),
    path('drafts/<int:pk>/', DraftDetail.as_view(), name='draft-detail'),
    path('drafts/<int:pk>/confirm/', confirm_draft, name='draft-confirm'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('posts/<int:pk>/like/', like, name='post-like'),

    path('', include(router.urls)),
    path('posts/<int:pk>/comments/create/', CommentViewSet.as_view({'post': 'create'}), name='comment-add'),
]
