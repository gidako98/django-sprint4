from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.urls import reverse
from django.utils import timezone

from blog.constants import POSTS_ON_PAGE
from blog.models import Post

User = get_user_model()


def paginator(request, queryset, posts_on_page=POSTS_ON_PAGE):
    """Пагинатор."""
    paginator = Paginator(queryset, posts_on_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


class CommentSuccessUrlMixin:
    """Миксин редиректа при добавлении комментария."""

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.object.post.id}
        )


class EditDeleteSuccessUrlMixin:
    """Миксин редиректа после редактирования или удаления поста."""

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username},
        )


class AuthorOrAdminRequiredMixin:
    """Миксин проверки авторства или администратора."""

    author_field = 'author'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()

        if hasattr(obj, 'username'):
            is_author = (request.user == obj)
        else:
            author = getattr(obj, self.author_field, None)
            is_author = (request.user == author)

        if not (is_author or request.user.is_staff):
            raise PermissionDenied(
                'У вас не достаточно прав для выполнения этого действия.'
            )
        return super().dispatch(request, *args, **kwargs)


def get_visible_posts_for_user(user=None, queryset=None, comment_count=False):
    """
    Функция для фильтрации доступных для просмотра публикаций в зависимости от
    типа пользователя и счетчик комментариев.
    """
    if queryset is None:
        queryset = Post.objects.all()
    queryset = queryset.select_related(
        'category', 'location', 'author',
    ).order_by(
        '-pub_date'
    )
    if comment_count:
        queryset = queryset.annotate(comment_count=Count('comments'))
    base_filter = Q(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )
    if user and user.is_superuser:
        return queryset
    elif user and user.is_authenticated:
        return queryset.filter(base_filter | Q(author_id=user.id))
    else:
        return queryset.filter(base_filter)
