# Generated by Django 5.0.3 on 2024-04-04 06:46

import common.utils
import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='заголовок')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='url')),
                ('content', django_ckeditor_5.fields.CKEditor5Field(verbose_name='текст статьи')),
                ('content_concise', models.TextField(max_length=120, verbose_name='краткое описание статьи')),
                ('image_url', models.ImageField(storage=common.utils.CustomStorage, upload_to='', verbose_name='изображение')),
                ('date', models.DateField(auto_now_add=True, verbose_name='дата')),
            ],
            options={
                'verbose_name': 'пост',
                'verbose_name_plural': 'посты',
            },
        ),
    ]
