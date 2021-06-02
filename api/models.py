from django.contrib.auth import get_user_model

from django.db import models

User = get_user_model()


class UserRole(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    titles = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='reviews'
    )
    review_name = models.CharField(
        max_length=300,
        verbose_name='Тема отзыва',
        help_text='Напишите тему отзыва',
    )
    review_discriprion = models.CharField(
        max_length=300,
        verbose_name='Описание отзыва',
        help_text='Напишите отзыв',

    )
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.CharField(
        max_length=300,
        verbose_name='Описание комментария',
        help_text='Напишите комментарий',
    )
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
