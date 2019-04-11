import shy.posts.forms as forms
from django.shortcuts import render, get_object_or_404, redirect
from shy.posts.models import Post


def home(request):
    posts = Post.objects.filter().order_by('-created_on')

    data = {
        "posts": posts
    }

    return render(request, 'public/home.html', data)


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
