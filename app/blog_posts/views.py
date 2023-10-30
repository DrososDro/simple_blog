from django.shortcuts import redirect, render
from django.contrib import messages

from accounts.decorators import is_auth
from blog_posts import forms
from blog_posts.models import BlogPost

# Create your views here.


def home(request):
    search = request.GET.get("query", None)
    if search != "" and search is not None:
        posts = BlogPost.objects.filter(title__icontains=search or " ")
    else:
        posts = BlogPost.objects.all()
    context = {
        "posts": posts,
    }
    return render(request, "blog_posts/posts.html", context)


def single_post(request, pk=None):
    try:
        id = int(pk)
        post = BlogPost.objects.get(pk=id)
    except (
        BlogPost.DoesNotExist,
        ValueError,
    ):
        return render(request, "404.html")

    context = {"post": post}

    return render(request, "blog_posts/single_post.html", context)


@is_auth
def create_post(request):
    form = forms.PostsForm()

    if request.method == "POST":
        form = forms.PostsForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            messages.success(request, "Post successfully created")
            return redirect("home")

    context = {
        "form": form,
        "blog_title": "Create Post",
        "blog_button": "Create Post",
    }
    return render(request, "blog_posts/create_post.html", context)


@is_auth
def my_articles(request):
    user = request.user
    posts = user.blogpost_set.all()

    context = {"posts": posts}
    return render(request, "blog_posts/my_posts.html", context)


@is_auth
def delete_article(request, pk=None):
    user = request.user
    try:
        pk = int(pk)
        post = user.blogpost_set.get(pk=pk)

    except (BlogPost.DoesNotExist, ValueError):
        return render(request, "404.html")
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post successfully Deleted")
        return redirect("my_articles")

    context = {"post": post, "delete_message": f"Post {post.title}"}

    return render(request, "delete.html", context)


@is_auth
def update_post(request, pk=None):
    user = request.user
    try:
        pk = int(pk)
        post = user.blogpost_set.get(pk=pk)
    except (BlogPost.DoesNotExist, ValueError):
        return render(request, "404.html")
    form = forms.PostsForm(instance=post)

    if request.method == "POST":
        form = forms.PostsForm(request.POST, instance=post)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            messages.success(request, "Post successfully updated")
            return redirect("post", form.pk)

    context = {
        "form": form,
        "blog_title": "Update Post",
        "blog_button": "Update Post",
    }
    return render(request, "blog_posts/create_post.html", context)
