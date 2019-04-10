from django.shortcuts import render, get_object_or_404
from shy.posts.models import Post


def home(request):
    posts = Post.objects.all()

    data = {
        "posts": posts
    }

    return render(request, 'public/home.html', data)


def single_post(request, uuid=None):
    if uuid:
        post = get_object_or_404(Post, uuid=uuid)
    else:
        post = Post.objects.last()

    data = {
        "post": post
    }

    return render(request, 'public/post.html', data)
