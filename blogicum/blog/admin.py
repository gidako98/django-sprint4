from typing import Any

from django.contrib import admin

from blog.models import Category, Comment, Location, Post


class PublishActionAdminPanelMixin:
    """Миксин добавления в админ-панель действия 'Опубликовать/Скрыть'."""

    SHORT_TEXT_LENGHT = 30

    def _shorted_text_impl(self, obj: Any) -> str:
        """Реализация сокращения текста."""
        text = getattr(obj, 'text', str(obj))
        return (
            text[:self.SHORT_TEXT_LENGHT] + '...'
            if len(text) > self.SHORT_TEXT_LENGHT else text
        )

    @admin.display(description='Текст')
    def shorted_text(self, obj: Any) -> str:
        return self._shorted_text_impl(obj)

    @admin.action(description='Опубликовать выбранные элементы')
    def published(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description='Снять с публикации выбранные элементы')
    def unpublished(self, request, queryset):
        queryset.update(is_published=False)


@admin.register(Post)
class PostAdmin(PublishActionAdminPanelMixin, admin.ModelAdmin):
    """Модель Публикации для админ-панели."""

    list_display = (
        'title', 'shorted_text', 'author', 'category',
        'location', 'is_published', 'pub_date'
    )
    search_fields = [
        'title__icontains',
        'author__username',
        'location__name',
        'category__title'
    ]
    list_filter = (
        'is_published', 'author', 'category', 'location', 'pub_date'
    )
    list_editable = ('is_published',)
    actions = ['published', 'unpublished']

    def get_queryset(self, request):
        """Оптимизация обращений к базе данных."""
        return super().get_queryset(request).select_related(
            'author', 'category', 'location',
        )


@admin.register(Category)
class CategoryAdmin(PublishActionAdminPanelMixin, admin.ModelAdmin):
    """Модель Категория для админ-панели."""

    search_fields = [
        'title__icontains',
    ]
    list_display = ('title', 'is_published', 'created_at')
    list_editable = ('is_published',)
    actions = ['published', 'unpublished']


@admin.register(Location)
class LocationAdmin(PublishActionAdminPanelMixin, admin.ModelAdmin):
    """Модель Местоположение для админ-панели."""

    search_fields = [
        'name__icontains',
    ]
    list_display = ('name', 'is_published', 'created_at')
    list_editable = ('is_published',)
    actions = ['published', 'unpublished']


@admin.register(Comment)
class CommentAdmin(PublishActionAdminPanelMixin, admin.ModelAdmin):
    """Модель Комментария для админ-панели."""

    search_fields = [
        'post__title__icontains',
        'text',
        'author__username',
    ]
    list_display = (
        'post', 'shorted_text', 'author', 'is_published', 'created_at'
    )
    list_filter = ('is_published', 'author', 'post', 'created_at')
    list_editable = ('is_published',)
    actions = ['published', 'unpublished']

    def get_queryset(self, request):
        """Оптимизация обращений к базе данных."""
        return super().get_queryset(request).select_related(
            'author', 'post',
        )
