# Generated by Django 4.2.4 on 2023-09-04 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_post_post_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_md',
        ),
    ]