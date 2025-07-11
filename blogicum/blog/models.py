from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from abstract.models import PublishedModel
from blog.constants import NAME_SLICE

User = get_user_model()


class Location(PublishedModel):
    """Модель "Местоположение"."""

    name = models.CharField('Название места', max_length=256)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:NAME_SLICE]


class Category(PublishedModel):
    """Модель "Категория"."""

    title = models.CharField('Заголовок', max_length=256)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; разрешены символы '
            'латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:NAME_SLICE]
    posts = models.ManyToManyField(
        'Post',
        related_name='category_posts',
        verbose_name='Посты категории',
        blank=True
    )


class Post(PublishedModel):
    """Модель "Публикация"."""

    title = models.CharField('Заголовок', max_length=256)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — можно делать '
            'отложенные публикации.'
        ),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,
    )
    location = models.ForeignKey(
        Location,
        verbose_name='Местоположение',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        related_name='post_category',
    )
    image = models.ImageField('Фото', upload_to='posts_images', blank=True)

    class Meta:
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title[:NAME_SLICE]

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.pk})


class Comment(PublishedModel):
    """Модель "Комментарий"."""

    text = models.TextField('Комментарий')
    post = models.ForeignKey(
        Post,
        verbose_name='Публикация',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Создано'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор',
        related_name='comments',
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f"Комментарий #{self.id} к посту '{self.post}'"
