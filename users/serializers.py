from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Profile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'groups']
        ordering = ['-id']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
        ordering = ['-id']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'url', 'user', 'image', 'bio', 'city', 'birth_date']
        ordering = ['-id']

    def create(self, validated_data):
        """
        Create and return a new `Profile` instance, given the validated data.
        """
        return Profile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.user = validated_data.get('user', instance.user)
        instance.image = validated_data.get('image', instance.image)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.city = validated_data.get('city', instance.city)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.save()
        return instance
