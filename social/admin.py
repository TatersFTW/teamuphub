from django.contrib import admin
from .models import Profile, Post, Comment, Friendship, GameAvailability

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Friendship)
admin.site.register(GameAvailability)
