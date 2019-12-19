from datetime import timedelta, date
from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from .models import Post, Comment, Draft
from .permissions import IsOwnerOrReadOnly, IsSenderOrReadOnly
from .serializers import PostSerializer, CommentSerializer, DraftSerializer


class DraftCreation(generics.CreateAPIView):
    queryset = Draft.objects.all()
    serializer_class = DraftSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)


class DraftList(generics.ListAPIView):
    queryset = Draft.objects.all()
    serializer_class = DraftSerializer


class DraftDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Draft.objects.all()
    serializer_class = DraftSerializer
    permission_classes = (IsOwnerOrReadOnly, )


class PostCreation(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)
        if 'pk' in self.kwargs:
            Draft.objects.filter(id=self.kwargs['pk']).delete()


class PostList(generics.ListAPIView):
    serializer_class = PostSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['id', 'title', 'created_at', 'updated_at', 'author', 'likes_number']

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Post.objects.all().order_by('-created_at')

        if 'period' in self.kwargs:
            today = timezone.now()
            if self.kwargs['period'] == 'month':
                queryset = queryset.filter(created_at__year=today.year,
                                           created_at__month=today.month)
            elif self.kwargs['period'] == 'week':
                week_ago = date.today() - timedelta(days=7)
                queryset = queryset.filter(created_at__range=(week_ago, today))
            elif self.kwargs['period'] == 'day':
                queryset = queryset.filter(created_at__year=today.year,
                                           created_at__month=today.month,
                                           created_at__day=today.day)

        author_id = self.request.query_params.get('author_id', None)
        if author_id is not None:
            queryset = queryset.filter(author=author_id)
        return queryset


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly, )

    def perform_update(self, serializer):
        updated_at = timezone.now()
        serializer.save(updated_at=updated_at)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsSenderOrReadOnly)
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        sender = self.request.user
        serializer.save(post=post, sender=sender)


class PostLike(APIView):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        Post.like_post(post, user)
        return redirect('post-detail', post.id)
