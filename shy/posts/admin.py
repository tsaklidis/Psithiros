from django.contrib import admin

from shy.posts.models import Post, Answers


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('id', 'created_on')


@admin.register(Answers)
class AnsAdmin(admin.ModelAdmin):
    model = Answers
    list_display = ('parent', 'created_on')
