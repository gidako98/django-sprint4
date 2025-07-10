from django.db import models


M_CHAR_LENGHT = 256


class TitleModel(models.Model):
    title = models.CharField(
        max_length=M_CHAR_LENGHT,
        blank=False,
        verbose_name="Заголовок",
    )

    class Meta:
        abstract = True


class CoreModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    class Meta:
        abstract = True
