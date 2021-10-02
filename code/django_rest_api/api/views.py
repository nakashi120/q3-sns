from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from . import serializers
from .models import Profile, Post, Comment


class CreateUserView(generics.CreateAPIView):
    """Create user view"""
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)


class ProfileViewSet(viewsets.ModelViewSet):
    """Manage profiles in the database"""
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def perform_create(self, serializer):
        """Create a user object"""
        serializer.save(user_profile=self.request.user)


class MyProfileListView(generics.ListAPIView):
    """List view for my profile"""
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        return self.queryset.filter(user_profile=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    """Manage Posts in the database"""
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        serializer.save(user_post=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Manage Comments in the database"""
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user_comment=self.request.user)
