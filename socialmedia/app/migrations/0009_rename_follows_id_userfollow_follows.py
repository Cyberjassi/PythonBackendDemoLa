# Generated by Django 5.0.2 on 2024-03-15 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_userfollow'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userfollow',
            old_name='follows_id',
            new_name='follows',
        ),
    ]
