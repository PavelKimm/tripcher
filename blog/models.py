from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class Post(models.Model):
    title = models.CharField(max_length=80)
    image = models.ImageField(default='post_pics/test.png', upload_to='post_pics')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

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


class Draft(models.Model):
    title = models.CharField(max_length=80)
    image = models.ImageField(default='post_pics/test.png', upload_to='post_pics')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

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
