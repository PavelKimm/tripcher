from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ('url', 'username', 'image', 'bio', 'city', 'birth_date')
        ordering = ('-id',)

    def create(self, validated_data):
        """
        Create and return a new `Profile` instance, given the validated data.
        """
        return Profile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Profile` instance, given the validated data.
        """
        instance.image = validated_data.get('image', instance.image)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.city = validated_data.get('city', instance.city)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.save()
        return instance


class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('url', 'friends')
        ordering = ('-id',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']
        ordering = ['-id']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
        ordering = ['-id']
