from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from core.models import CoreModel, TitleModel


USER = get_user_model()
M_CHAR_LENGHT = 256


class IsPublished(models.Manager):
    def published(self):
        return super().get_queryset().filter(
            pub_date__lte=timezone.now(),
            is_published=True,
        )


class Category(CoreModel, TitleModel):
    description = models.TextField(blank=False, verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
        'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )

    objects = IsPublished()

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Location(CoreModel):
    name = models.CharField(
        max_length=M_CHAR_LENGHT,
        blank=False,
        default='Планета Земля',
        verbose_name="Название места",
    )

    objects = IsPublished()

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Post(CoreModel, TitleModel):
    text = models.TextField(blank=False, verbose_name='Текст')
    image = models.ImageField('Фото', upload_to='posts_images', blank=True)
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем '
        '— можно делать отложенные публикации.',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Категория',
    )
    author = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Местоположение',
    )

    objects = IsPublished()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Comment(CoreModel):
    text = models.TextField(blank=False, verbose_name='Текст комментария')
    author = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Автор комментария',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Комментируемый пост',
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        # От старых к новым как написано в задании!
        ordering = ('author', '-created_at',)

    def __str__(self):
        return self.text
