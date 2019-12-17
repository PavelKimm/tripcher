from django.contrib.auth.models import User, Group, Permission
from django.db.models import Q
from rest_framework import serializers
from rest_framework import fields
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Profile
        fields = ('url', 'username', 'image', 'bio', 'city', 'birth_date', 'friends')
        read_only_fields = ('friends', )

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


class UserCreationSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'password']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']


# class UserLoginSerializer(ModelSerializer):
#     token = fields.CharField(allow_blank=True, read_only=True)
#     username = fields.CharField(required=False, allow_blank=True)
#     # email = fields.EmailField(label='E-mail', required=False, allow_blank=True)
#
#     class Meta:
#         model = User
#         fields = ['username', 'password', 'token']
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def validate(self, data):
#         user_obj = None
#         # email = data.get('email', None)
#         username = data.get('username', None)
#         password = data['password']
#         if not username:
#             raise ValidationError('A username is required to login.')
#
#         user = User.objects.filter(
#             Q(username=username)
#         ).distinct()
#         if user.exists() and user.count() == 1:
#             user_obj = user.first()
#         else:
#             raise ValidationError('This username is not valid.')
#
#         if user_obj:
#             if not user_obj.check_password(password):
#                 raise ValidationError('Incorrect credentials! Try again.')
#
#         data['token'] = 'some token'
#         return data


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
