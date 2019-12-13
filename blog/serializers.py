from rest_framework import serializers
from . import models


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ('url', 'post', 'sender', 'content')
        read_only_fields = ('post', 'sender')


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = models.Post
        fields = ('url', 'author', 'title', 'image', 'content',
                  'created_at', 'updated_at', 'likes_number',
                  'users_liked', 'comments')
        read_only_fields = ('author', 'created_at', 'updated_at',
                            'likes_number', 'users_liked')


class DraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Draft
        fields = ('url', 'author', 'title', 'image', 'content',
                  'created_at', 'updated_at')
        read_only_fields = ('created_at', 'author')
