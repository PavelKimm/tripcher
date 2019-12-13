from django.urls import path, include
from rest_framework import routers

from .views import (PostCreation, PostList, PostDetail,
                    CommentViewSet, like, DraftCreation,
                    DraftList, DraftDetail)

router = routers.DefaultRouter()
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('posts/', PostList.as_view(), name='posts-list'),
    path('posts/create/', PostCreation.as_view(), name='post-creation'),
    path('posts/create/save_as_draft/', DraftCreation.as_view(), name='draft-creation'),

    path('drafts/', DraftList.as_view(), name='drafts-list'),
    path('drafts/<int:pk>/', DraftDetail.as_view(), name='draft-detail'),
    path('drafts/<int:pk>/confirm/', PostCreation.as_view(), name='draft-confirmation'),

    path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('posts/<int:pk>/like/', like, name='post-like'),

    path('', include(router.urls)),
    path('posts/<int:pk>/comments/create/', CommentViewSet.as_view({'post': 'create'}), name='comment-add'),
]
