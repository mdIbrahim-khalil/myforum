# Generated by Django 2.2.17 on 2023-06-08 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_forum_app', '0003_post_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='is_locked',
        ),
    ]
