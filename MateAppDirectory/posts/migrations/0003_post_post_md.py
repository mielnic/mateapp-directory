# Generated by Django 4.2.4 on 2023-09-02 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_post_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_md',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
    ]