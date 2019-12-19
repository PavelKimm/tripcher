from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import F
from django.urls import reverse
from users.models import Profile
from utils import image_utils


class Post(models.Model):
    title = models.CharField(max_length=80)
    image = models.ImageField(default='post_pics/test.png', upload_to='post_pics')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    users_liked = models.ManyToManyField(User, blank=True)
    likes_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image_utils.resize(self.image.path, 1000)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def like_post(self, user):
        if user not in self.users_liked.all():
            self.likes_number = F('likes_number') + 1
            self.users_liked.add(user)
            self.save()


class Draft(models.Model):
    title = models.CharField(max_length=80)
    image = models.ImageField(default='post_pics/test.png', upload_to='post_pics')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} (draft)'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image_utils.resize(self.image.path, 1000)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    sender = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return f'{self.sender}: {self.content}'
