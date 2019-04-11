from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

import re
import shy.posts.forms as forms

from shy.posts.models import Post


def _clean_search_post(data):
    """Ensure data is valid."""
    if data:
        if not re.match(r'(^[\w\s.]+$)', data, re.UNICODE):
            return None
        return data
    return None


def home(request):
    posts = Post.objects.filter().order_by('-created_on')

    data = {
        "posts": posts
    }

    return render(request, 'public/home.html', data)


def info(request):
    return render(request, 'public/info.html')


def single_post(request, uuid=None):
    status = False
    if uuid:
        post = get_object_or_404(Post, uuid=uuid)
    else:
        post = Post.objects.last()

    ans_form = forms.AnswersForm(request.POST or None)
    if ans_form.is_valid():
        ans_new = ans_form.save(commit=False)
        ans_new.parent = post
        ans_new.save()
        status = True
        # return redirect('posts:single_post', post.uuid)
    else:
        # print(ans_form.errors)
        pass

    data = {
        "post": post,
        "ans_form": ans_form,
        "status": status
    }

    return render(request, 'public/post.html', data)


def new_post(request):

    post_form = forms.PostForm(request.POST or None)
    if post_form.is_valid():
        post = post_form.save(commit=False)
        post.save()
        return redirect('posts:single_post', post.uuid)
    else:
        # print(ans_form.errors)
        pass

    data = {
        "post_form": post_form,
    }

    return render(request, 'public/new_post.html', data)


@require_POST
def search(request):
    value = _clean_search_post(request.POST.get('search_term'))
    if value:
        try:
            post = Post.objects.get(uuid=value)
            return redirect('posts:single_post', post.uuid)
        except Post.DoesNotExist:
            posts = Post.objects.filter(text__icontains=value)

        data = {
            "posts": posts
        }

        return render(request, 'public/search_results.html', data)
    else:
        data = {
            "posts": ''
        }
        return render(request, 'public/search_results.html', data)
