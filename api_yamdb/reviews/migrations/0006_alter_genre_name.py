# Generated by Django 3.2 on 2023-04-06 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_alter_category_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Название жанра'),
        ),
    ]
