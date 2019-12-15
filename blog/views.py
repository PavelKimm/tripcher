from datetime import timedelta, date, datetime, time
from django.shortcuts import redirect

from rest_framework import generics, viewsets
from django.utils import timezone
from .models import Post, Comment, Draft
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly, IsSenderOrReadOnly
from .serializers import PostSerializer, CommentSerializer, DraftSerializer
from rest_framework.filters import OrderingFilter
from django.db.models.functions import ExtractMonth, ExtractWeek, ExtractDay


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
            today = date.today()
            if self.kwargs['period'] == 'month':
                queryset = queryset.filter(created_at__year=today.year,
                                           created_at__month=today.month)
            elif self.kwargs['period'] == 'week':
                week_ago = today - timedelta(days=7)
                # today_max = today + timedelta(days=1)
                today_max = datetime.combine(today, time.max)
                queryset = queryset.filter(created_at__range=(week_ago, today_max))
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
        post = Post.objects.get(pk=self.kwargs['pk'])
        sender = self.request.user
        serializer.save(post=post, sender=sender)

    # def perform_destroy(self, instance):
    #     instance = Comment.objects.get(pk=self.kwargs['comment_id'])
    #     instance.delete()
    #
    # def partial_update(self, request, *args, **kwargs):
    #     instance = Comment.objects.get(pk=self.kwargs['comment_id'])
    #     serializer = self.serializer_class(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)


def like(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user
    Post.like_post(post, user)
    return redirect('post-detail', post.id)
