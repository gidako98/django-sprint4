from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DeleteView, DetailView, UpdateView

from blog.models import Category, Comment, Post
from blog.utils import (
    AuthorOrAdminRequiredMixin,
    CommentSuccessUrlMixin,
    EditDeleteSuccessUrlMixin,
    get_visible_posts_for_user,
    paginator,
)
from users.forms import CommentForm, CreatePostForm, MyChangeForm

User = get_user_model()


def index(request):
    """Главная страница сайта."""
    post_list = get_visible_posts_for_user(
        comment_count=True
    )
    page_obj = paginator(request, post_list)
    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


def category_posts(request, category_slug):
    """Отображает категорию записи."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    posts = get_visible_posts_for_user(
        queryset=category.post_category.all(),
        comment_count=True,
    )
    page_obj = paginator(request, posts)
    context = {
        'page_obj': page_obj,
        'category': category,
    }
    return render(request, 'blog/category.html', context)


@login_required
def create_edit_post(request, post_id=None):
    """Создание новой или редактирование записи"""
    post = None
    if post_id:
        post = get_object_or_404(Post, id=post_id)
        if post.author != request.user:
            return redirect('blog:post_detail', post_id=post.id)
    form = CreatePostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    if form.is_valid():
        new_post = form.save(commit=False)
        if not post:
            new_post.author = request.user
        new_post.save()
        return redirect('blog:profile', username=request.user.username)
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'blog/create.html', context)


class PostDetailView(DetailView):
    """CBV детального просмотра поста."""

    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):
        queryset = get_visible_posts_for_user(self.request.user)
        return get_object_or_404(queryset, pk=self.kwargs['post_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class AddCommentView(LoginRequiredMixin, DetailView):
    """CBV добавления комментария."""

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, is_published=True)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', post_id=post.id)


class PostDeleteView(
    LoginRequiredMixin,
    AuthorOrAdminRequiredMixin,
    EditDeleteSuccessUrlMixin, DeleteView
):
    """CBV удаления поста."""

    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'


class ProfileDetailView(DetailView):
    """CBV просмотра профиля пользователя."""

    model = User
    template_name = 'blog/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        author_posts = Post.objects.filter(author=profile_user)
        visible_posts = get_visible_posts_for_user(
            user=self.request.user,
            queryset=author_posts,
            comment_count=True,
        ).order_by('-pub_date')
        page_obj = paginator(self.request, visible_posts)
        context.update({
            'page_obj': page_obj,
            'profile': profile_user,
        })
        return context


class EditProfileView(
    LoginRequiredMixin,
    EditDeleteSuccessUrlMixin, UpdateView
):
    """CBV редактирования профиля пользователя."""

    model = User
    form_class = MyChangeForm
    template_name = 'registration/profile_edit.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user


class EditCommentView(
    LoginRequiredMixin,
    AuthorOrAdminRequiredMixin,
    CommentSuccessUrlMixin, UpdateView,
):
    """CBV редактирования комментария."""

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'


class DeleteCommentView(
        LoginRequiredMixin,
        AuthorOrAdminRequiredMixin,
        CommentSuccessUrlMixin,
        DeleteView,
):
    """CBV удаления комментария"""

    model = Comment
    template_name = 'blog/comment.html'
