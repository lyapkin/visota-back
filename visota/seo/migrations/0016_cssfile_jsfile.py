# Generated by Django 5.0.3 on 2024-10-01 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0015_metagenerationrule_metagenerationruletranslation'),
    ]

    operations = [
        migrations.CreateModel(
            name='CSSFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='название')),
                ('content', models.TextField(verbose_name='код')),
            ],
            options={
                'verbose_name': 'css',
                'verbose_name_plural': 'css',
            },
        ),
        migrations.CreateModel(
            name='JSFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='название')),
                ('content', models.TextField(verbose_name='код')),
            ],
            options={
                'verbose_name': 'js',
                'verbose_name_plural': 'js',
            },
        ),
    ]
