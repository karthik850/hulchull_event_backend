# Generated by Django 4.2.17 on 2024-12-27 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventinfoapp', '0004_importantpersons'),
    ]

    operations = [
        migrations.RenameField(
            model_name='importantpersons',
            old_name='ender',
            new_name='gender',
        ),
    ]
