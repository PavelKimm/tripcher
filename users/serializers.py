from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers
from .models import Profile


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


class ProfileSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(source='user.username')
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Profile
        fields = ['url', 'user', 'image', 'bio', 'city', 'birth_date']
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


class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token and provider.
    """
    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)

    # def create(self, validated_data):
    #     """
    #     Create and return a new `User` instance, given the validated data.
    #     """
    #     return User.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.username = validated_data.get('user', instance.username)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.save()
    #     return instance
