from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=500, blank=True)
    city = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    friends = models.ManyToManyField('self', symmetrical=False,
                                     related_name='friends+')

    def __str__(self):
        return f'{self.user.username}\'s profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        max_size = 300
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

    @classmethod
    def make_friend(cls, from_profile, to_profile):
        friend, created = cls.objects.get_or_create(
            user=from_profile
        )
        friend.friends.add(to_profile)

    @classmethod
    def remove_friend(cls, from_profile, to_profile):
        friend, created = cls.objects.get_or_create(
            user=from_profile
        )
        friend.friends.remove(to_profile)
