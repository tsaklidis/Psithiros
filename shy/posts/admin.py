from django.contrib import admin

from shy.posts.models import Post


@admin.register(Post)
class CarAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('id', 'created_on')
