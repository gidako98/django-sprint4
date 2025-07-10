from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CommentForm, PostForm
from .models import Category, Post, USER, Comment
from user.forms import EditUserForm
from utils.utils import paginator


POSTS_ON_PAGE = 10


def index(request):
    post = (
        Post.objects.published()
        .filter(category__is_published=True)
        .annotate(comment_count=Count('comment'))
        .order_by('-pub_date')
    )
    page_obj = paginator(post, request, POSTS_ON_PAGE)
    return render(
        request, 'blog/index.html', {'page_obj': page_obj, 'post': post}
    )


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related('category', 'author', 'location'),
        pk=post_id,
    )

    is_author = request.user.is_authenticated and post.author == request.user
    is_valid = (
        post.is_published
        and post.category.is_published
        and post.pub_date <= timezone.now()
    )

    if not (is_author or is_valid):
        raise Http404("Пост не найден.")

    comments = Comment.objects.filter(post=post).order_by('created_at')
    form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'user': request.user,
    }
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category.objects.filter(is_published=True), slug=category_slug
    )
    post = (
        Post.objects.published()
        .annotate(comment_count=Count('comment'))
        .filter(
            category__slug=category_slug,
        )
        .order_by('-pub_date')
    )

    page_obj = paginator(post, request, POSTS_ON_PAGE)
    context = {'post': post, 'category': category, 'page_obj': page_obj}
    return render(request, 'blog/category.html', context)


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
    else:
        form = EditUserForm(instance=user)

    return render(request, 'blog/user.html', {'form': form})


def author_profile(request, author):
    profile = get_object_or_404(USER, username=author)

    post = Post.objects.annotate(comment_count=Count('comment')).filter(
        author=profile
    ).order_by('-pub_date')

    if request.user.is_authenticated and request.user == profile:
        post = post.order_by('-pub_date')
    else:
        post = post.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        )

    page_obj = paginator(post, request, POSTS_ON_PAGE)
    content = {'page_obj': page_obj, 'profile': profile}
    return render(request, 'blog/profile.html', content)


@login_required
def comment(request, post_id, id=None):
    post = get_object_or_404(Post, pk=post_id)
    if id is not None:
        comment = get_object_or_404(Comment, pk=id, post=post)
        if comment.author != request.user:
            return redirect('blog:post_detail', post_id=post_id)
    else:
        comment = None

    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('blog:post_detail', post_id=post_id)
    return render(
        request,
        'blog/comment.html',
        {'form': form, 'comment': comment, 'post': post},
    )


@login_required
def delete_comment(request, post_id, id):
    comment = get_object_or_404(Comment, pk=id, post_id=post_id)
    if request.user != comment.author:
        return redirect('blog:post_detail', post_id=post_id)

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)

    return render(request, 'blog/comment.html')


@login_required
def post(request, post_id=None):
    user = request.user
    if post_id is not None:
        post = get_object_or_404(Post, pk=post_id)
        if post.author != user:
            return redirect('blog:post_detail', post_id=post_id)
    else:
        post = None

    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:profile', author=user)
    else:
        form = PostForm(instance=post)

    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required
def delete_post(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST or None, instance=post)
    if post.author != request.user:
        return redirect('blog:index')

    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile', author=user)

    return render(request, 'blog/create.html', {'form': form})


@login_required
def custom_logout(request):
    logout(request)
    return render(request, 'registration/logged_out.html')
