# Generated by Django 5.0.6 on 2024-07-04 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_badge_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonprogress',
            name='locked',
            field=models.BooleanField(default=False),
        ),
    ]
