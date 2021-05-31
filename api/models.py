from django.contrib.auth import get_user_model

from django.db import models

User = get_user_model()


class Categories(models.Model):
    category_name = models.CharField(
        max_length=50,
        verbose_name='Название категории',
        help_text='Напишите название новой категории',
    )
    category_description = models.TextField(
        verbose_name='Описание категории',
        help_text='Дайте краткое опишисание новой категории'
    )

    class Meta:
        ordering = ['-category_name']


class Genres(models.Model):
    genre_name = models.CharField(
        max_length=50,
        verbose_name='Название жанра',
        help_text='Напишите название нового жанра',
    )
    genre_description = models.TextField(
        verbose_name='Описание жанра',
        help_text='Дайте краткое опишисание нового жанра'
    )

    class Meta:
        ordering = ['-genre_name']


class Titles(models.Model):
    title_name = models.TextField(
        verbose_name='Название произведения',
        help_text='Напишите здесь название нового произведения',
    )
    title_description = models.TextField(
        verbose_name='Описание произведения',
        help_text='Напишите здесь название нового произведения',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации произведения',
        auto_now_add=True,
    )
    category = models.ForeignKey(
        'Categories',
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Категория произведения',
        help_text='Выберите категорию добавляемого произведения'
    )
    genre = models.ForeignKey(
        'Genres',
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Жанр произведения',
        help_text='Выберите жанр добавляемого произведения'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор произведения'
    )
    image = models.ImageField(
        upload_to='titles/',
        blank=True,
        null=True,
        help_text='Вставьте изображение для своего произведения'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title_name', 'category'],
                name='unigue_category'
            ),
        ]
        ordering = ['-pub_date']

    def __str__(self):
        return self.title_name[:15]
