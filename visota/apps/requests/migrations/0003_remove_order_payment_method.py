# Generated by Django 5.0.3 on 2024-04-24 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0002_samplerequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payment_method',
        ),
    ]