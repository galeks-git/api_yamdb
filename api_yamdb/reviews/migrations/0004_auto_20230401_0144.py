# Generated by Django 3.2 on 2023-04-01 01:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_remove_comment_score'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='created',
            new_name='pub_date',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='created',
            new_name='pub_date',
        ),
    ]