from django.shortcuts import redirect
from rest_framework import generics, viewsets
from django.utils import timezone
from .models import Post, Comment, Draft
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
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
    queryset = Post.objects.all()
    serializer_class = PostSerializer


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


class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


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


def confirm_draft(request):
    pass


def like(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user
    Post.like_post(post, user)
    return redirect('post-detail', post.id)
