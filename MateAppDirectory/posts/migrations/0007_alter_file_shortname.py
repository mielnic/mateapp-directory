# Generated by Django 4.2.4 on 2023-09-08 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_file_color_file_ext_file_shortname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='shortName',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
