from rest_framework import serializers
from . import models


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ('id', 'post', 'sender', 'content')
        read_only_fields = ('post', 'sender')


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = models.Post
        fields = ('id', 'author', 'title', 'image', 'content',
                  'created_at', 'updated_at', 'likes_number',
                  'users_liked', 'comments')
        read_only_fields = ('created_at', 'author',
                            'likes_number', 'users_liked')
        ordering = ('-id', )


class DraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Draft
        fields = ('id', 'author', 'title', 'image', 'content',
                  'created_at', 'updated_at')
        read_only_fields = ('created_at', 'author')
        ordering = ('-id', )
