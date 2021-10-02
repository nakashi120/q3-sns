from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Post, Comment


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user object"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        user = get_user_model().objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for profile object"""
    created_on = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'nickname', 'user_profile', 'created_on', 'img')
        extra_kwargs = {'user_profile': {'read_only': True}}


class PostSerializer(serializers.ModelSerializer):
    """Serializer for post object"""
    created_on = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'user_post', 'created_on', 'img', 'liked')
        extra_kwargs = {'user_post': {'read_only': True}}


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comment object"""

    class Meta:
        model = Comment
        fields = ('id', 'text', 'user_comment', 'post')
        extra_kwargs = {'user_comment': {'read_only': True}}
