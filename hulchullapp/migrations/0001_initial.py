# Generated by Django 4.2.17 on 2024-12-25 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SecretCodeDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fav_number', models.IntegerField()),
                ('associate_name', models.CharField(max_length=255)),
                ('user_name', models.CharField(blank=True, max_length=255, null=True)),
                ('is_opened', models.BooleanField(default=False)),
                ('opened_on', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
