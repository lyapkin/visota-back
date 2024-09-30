# Generated by Django 5.0.3 on 2024-09-29 14:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_posttranslation_last_modified'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostRedirectFrom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_slug', models.CharField(max_length=60, unique=True, verbose_name='старый url')),
                ('lang', models.CharField(choices=[('ru', 'Русский'), ('en', 'Английский'), ('tr', 'Турецкий'), ('zh', 'Китайский')], default='ru', max_length=2, verbose_name='языковая версия поста старого url')),
                ('to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post')),
            ],
            options={
                'verbose_name': 'Старый слаг',
                'verbose_name_plural': 'Старые слаги',
            },
        ),
    ]