from django.contrib.auth import get_user_model

from django.db import models

User = get_user_model()


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
    review_discriprion = models.TextField(
        verbose_name='Описание отзыва',
        help_text='Напишите отзыв',

    )
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )


class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    titles = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField(
        verbose_name='Описание комментария',
        help_text='Напишите комментарий',
    )
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
