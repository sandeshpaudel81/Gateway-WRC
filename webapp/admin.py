from django.contrib import admin

from .models import Post, Profile

admin.site.site_header = "Gateway WRC Admin Dashboard"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass