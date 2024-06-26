# Generated by Django 5.0.3 on 2024-04-08 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_actual_price_alter_product_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charvalue',
            name='value',
            field=models.CharField(max_length=50, verbose_name='значение характеристики'),
        ),
        migrations.AlterUniqueTogether(
            name='charvalue',
            unique_together={('char', 'value')},
        ),
    ]
