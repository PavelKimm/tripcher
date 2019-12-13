from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from users.models import Profile


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
        img = Image.open(self.image.path)
        max_size = 1000
        if img.height > max_size:
            h_percent = max_size / float(img.size[1])
            w_size = int(float(img.size[0]) * h_percent)
            img.thumbnail((w_size, max_size))
            img.save(self.image.path)
        if img.width > max_size:
            w_percent = max_size / float(img.size[0])
            h_size = int(float(img.size[1]) * w_percent)
            img.thumbnail((max_size, h_size))
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def like_post(self, user):
        if user not in self.users_liked.all():
            self.likes_number = Post.objects.get(id=self.id).likes_number + 1
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
        img = Image.open(self.image.path)
        max_size = 1000
        if img.height > max_size:
            h_percent = max_size / float(img.size[1])
            w_size = int(float(img.size[0]) * h_percent)
            img.thumbnail((w_size, max_size))
            img.save(self.image.path)
        if img.width > max_size:
            w_percent = max_size / float(img.size[0])
            h_size = int(float(img.size[1]) * w_percent)
            img.thumbnail((max_size, h_size))
            img.save(self.image.path)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    sender = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return f'{self.sender}: {self.content}'
