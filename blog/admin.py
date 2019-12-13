from django.contrib import admin
from .models import Post, Draft, Comment


admin.site.register(Post)
admin.site.register(Draft)
admin.site.register(Comment)
