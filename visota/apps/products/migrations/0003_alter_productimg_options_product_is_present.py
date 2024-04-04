# Generated by Django 5.0.3 on 2024-04-03 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_charachteristics'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimg',
            options={'verbose_name': 'изображение товара', 'verbose_name_plural': 'изображения товара'},
        ),
        migrations.AddField(
            model_name='product',
            name='is_present',
            field=models.BooleanField(default=False, verbose_name='в наличии'),
        ),
    ]
