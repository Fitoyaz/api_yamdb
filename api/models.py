from django.contrib.auth.models import AbstractUser

from django.db import models

from django.db.models.deletion import CASCADE


class User(AbstractUser):
    ROLES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )
    role = models.CharField(max_length=50, choices=ROLES, default='user')
    bio = models.TextField(max_length=500, null=True)


class ConfCode(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=CASCADE,
        null=True, related_name='confcode'
    )
    email = models.EmailField(max_length=128)
    eml_conf_code = models.CharField(max_length=50)


class Categories(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название категории',
        help_text='Напишите название категории',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор категории'
    )
    category_description = models.TextField(
        verbose_name='Описание категории',
        help_text='Дайте краткое описание категории'
    )

    class Meta:
        ordering = ['name']


class Genres(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название жанра',
        help_text='Напишите название жанра',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор жанра'
    )
    genre_description = models.TextField(
        verbose_name='Описание жанра',
        help_text='Дайте краткое описание жанра'
    )

    class Meta:
        ordering = ['name']


class Titles(models.Model):
    name = models.TextField(
        verbose_name='Название',
        help_text='Напишите здесь название произведения',
    )
    year = models.DecimalField(
        max_digits=4,
        decimal_places=0,
        verbose_name='Год выпуска',
        help_text='Напишите здесь год выпуска произведения',
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Напишите здесь название произведения',
    )
    genre = models.ManyToManyField(
        'Genres',
        related_name='titles',
        symmetrical=False,
        db_table='title-genre-table',
        verbose_name='Slug жанра',
        help_text='Выберите жанр произведения'
    )
    category = models.ForeignKey(
        'Categories',
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Slug категории',
        help_text='Выберите категорию произведения'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category'],
                name='unigue_category'
            ),
        ]
        ordering = ['name']
