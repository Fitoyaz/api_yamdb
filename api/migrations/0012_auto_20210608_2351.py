# Generated by Django 3.0.5 on 2021-06-08 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20210608_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titles',
            name='year',
            field=models.IntegerField(help_text='Напишите здесь год выпуска произведения', verbose_name='Год выпуска'),
        ),
    ]
