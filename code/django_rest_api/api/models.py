from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


def upload_avatar_path(instance, filename):
    """Create filepath for saving avatar image"""
    ext = filename.split('.')[-1]
    return '/'.join(['avatars', str(instance.user_profile.id) + str(instance.nickname) + str('.') + str(ext)])


def upload_post_path(instance, filename):
    """Create filepath for saving post image"""
    ext = filename.split('.')[-1]
    return '/'.join(['posts', str(instance.user_post.id) + str(instance.title) + str('.') + str(ext)])


class UserManager(BaseUserManager):
    """Custom user manager model for using e-mail instead of username"""

    def create_user(self, email, password=None):
        """Create and saves a new User"""
        if not email:
            raise ValueError('User must have an e-mail address')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and saves a new super User"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Profile(models.Model):
    """Profile model"""
    nickname = models.CharField(max_length=30)
    user_profile = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='user_profile',
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)

    def __str__(self):
        return self.nickname


class Post(models.Model):
    """Post model"""
    title = models.CharField(max_length=100)
    user_post = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='user_post',
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_post_path)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked', blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=100)
    user_comment = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='user_comment',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
