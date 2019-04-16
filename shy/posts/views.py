from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

import re
import json
# import urllib
import urllib.request

import shy.posts.forms as forms

from shy.posts.models import Post, Answers


def _clean_search_post(data):
    """Ensure data is valid."""
    if data:
        if not re.match(r'(^[\w\s.]+$)', data, re.UNICODE):
            return None
        return data
    return None


def home(request):
    posts = Post.objects.filter().order_by('-created_on')

    paginator = Paginator(posts, 20)
    page = request.GET.get('page', 1)

    try:
        posts_paginated = paginator.page(page)
    except PageNotAnInteger:
        posts_paginated = paginator.page(1)
    except EmptyPage:
        posts_paginated = paginator.page(1)

    # Get the index of the current page
    # edited to something easier without index
    index = posts_paginated.number - 1
    # This value is maximum index of your pages, so the last page - 1
    max_index = len(paginator.page_range)
    # You want a range of 7, so lets calculate where to slice the list
    start_index = index - 7 if index >= 7 else 0
    end_index = index + 7 if index <= max_index - 7 else max_index
    # My new page range
    page_range = paginator.page_range[start_index:end_index]

    data = {
        "posts": posts_paginated,
        'page_range': page_range
    }

    return render(request, 'public/home.html', data)


def info(request):
    return render(request, 'public/info.html')


def terms(request):
    return render(request, 'public/terms.html')


def privacy(request):
    return render(request, 'public/privacy.html')


def single_post(request, uuid=None):
    status = False
    key = False
    if uuid:
        post = get_object_or_404(Post, uuid=uuid)
    else:
        post = Post.objects.last()

    ''' Begin reCAPTCHA validation '''
    recaptcha_response = request.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode()
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    ''' End reCAPTCHA validation '''

    ans_form = forms.AnswersForm(request.POST or None)
    if ans_form.is_valid() and result['success']:
        ans_new = ans_form.save(commit=False)
        ans_new.parent = post
        ans_new.save()
        status = True
        key = ans_new.uuid
        # return redirect('posts:single_post', post.uuid)
    else:
        # print(ans_form.errors)
        pass

    data = {
        "post": post,
        "ans_form": ans_form,
        "status": status,
        "key": key,
    }

    return render(request, 'public/post.html', data)


def new_post(request):
    ''' Begin reCAPTCHA validation '''
    recaptcha_response = request.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode()
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    ''' End reCAPTCHA validation '''

    post_form = forms.PostForm(request.POST or None)
    if post_form.is_valid() and result['success']:
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
    if value and len(value) > 2:

        if Post.objects.filter(uuid=value).exists():
            post = Post.objects.get(uuid=value)
            return redirect('posts:single_post', post.uuid)
        if Answers.objects.filter(uuid=value).exists():
            ans = Answers.objects.get(uuid=value)
            return redirect('posts:single_post', ans.parent.uuid)

        posts = Post.objects.filter(text__icontains=value)

        data = {
            "posts": posts
        }

        return render(request, 'public/search_results.html', data)
    else:
        data = {
            "posts": '',
        }
        return render(request, 'public/search_results.html', data)
