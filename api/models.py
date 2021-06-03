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
