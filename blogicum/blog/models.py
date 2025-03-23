from django.db import models
from django.contrib.auth import get_user_model
from .querysets import PostFilteredQuerySet
from typing import Union
from blogicum.settings import STR_SLICE, CHAR_FIELD_MAX_LENGTH


User = get_user_model()


class PublishedModel(models.Model):
    """Абстрактная модель. Добавляет флаг is_published."""

    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    class Meta:
        abstract = True


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания"""

    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True
    )

    class Meta:
        abstract = True


class Location(PublishedModel, CreatedModel):
    name = models.CharField(
        'Название места',
        max_length=CHAR_FIELD_MAX_LENGTH,
        default='Планета Земля'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        if len(self.name) > STR_SLICE:
            return self.name[:STR_SLICE] + '...'
        return self.name


class Category(PublishedModel, CreatedModel):
    title = models.CharField('Заголовок', max_length=CHAR_FIELD_MAX_LENGTH)
    description = models.TextField('Описание')
    slug = models.SlugField(
        unique=True,
        allow_unicode=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        indexes = [
            models.Index(fields=['slug'], name='slug_idx')
        ]

    def __str__(self):
        if len(self.title) > STR_SLICE:
            return self.title[:STR_SLICE] + '...'
        return self.title


class Post(PublishedModel, CreatedModel):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts'
    )
    location = models.ForeignKey(
        Location,
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )
    title = models.CharField('Заголовок', max_length=CHAR_FIELD_MAX_LENGTH)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время '
                  'в будущем — можно делать отложенные публикации.'
    )
    image = models.ImageField(
        'Фото', upload_to='posts_images', null=True, blank=True
    )
    objects: Union[
        PostFilteredQuerySet,
        models.QuerySet
    ] = PostFilteredQuerySet.as_manager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)
        default_related_name = 'posts'

    def __str__(self):
        if len(self.title) > STR_SLICE:
            return self.title[:STR_SLICE] + '...'
        return self.title


class Comment(CreatedModel):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        verbose_name='Пост',
        on_delete=models.CASCADE
    )
    text = models.TextField('Комментарий')

    class Meta(CreatedModel.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        default_related_name = 'comments'
        
    def __str__(self):
        if len(self.text) > STR_SLICE:
            return self.text[:STR_SLICE] + '...'
        return self.text
