# Generated by Django 5.0.2 on 2024-03-15 05:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='app.post'),
            preserve_default=False,
        ),
    ]