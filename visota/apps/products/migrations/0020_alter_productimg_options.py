# Generated by Django 5.0.3 on 2024-10-20 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_alter_productimg_options_productimg_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimg',
            options={'ordering': ('product', 'order', 'id'), 'verbose_name': 'изображение товара', 'verbose_name_plural': 'изображения товара'},
        ),
    ]