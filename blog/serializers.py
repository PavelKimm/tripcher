from rest_framework import serializers
from . import models


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    reply_set = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = models.Comment
        fields = ('id', 'url', 'content', 'sender', 'pub_date', 'parent', 'reply_set')
        read_only_fields = ('sender', 'pub_date')


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
