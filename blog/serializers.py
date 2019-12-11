from rest_framework import serializers
from . import models


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ('id', 'author', 'title', 'image', 'content', 'created_at', 'updated_at', )
        read_only_fields = ('created_at', 'author', )
        ordering = ('-id', )
