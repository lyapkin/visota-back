# Generated by Django 5.0.3 on 2024-09-30 07:04

import apps.products.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_categoryredirectfrom_productredirectfrom'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoryredirectfrom',
            options={'verbose_name': 'Старый слаг (редирект (seo))', 'verbose_name_plural': 'Старые слаги (редирект (seo))'},
        ),
        migrations.AlterModelOptions(
            name='productredirectfrom',
            options={'verbose_name': 'Старый слаг (редирект (seo))', 'verbose_name_plural': 'Старые слаги (редирект (seo))'},
        ),
        migrations.AlterField(
            model_name='producttranslation',
            name='slug',
            field=models.SlugField(blank=True, max_length=130, unique=True, validators=[apps.products.models.validate_is_product_slug_old], verbose_name='url'),
        ),
        migrations.AlterField(
            model_name='subcategorytranslation',
            name='slug',
            field=models.SlugField(blank=True, max_length=60, unique=True, validators=[apps.products.models.validate_is_category_slug_old], verbose_name='url'),
        ),
    ]