# Generated by Django 5.0.6 on 2024-06-27 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_courseenrollment_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='badge',
            name='code',
            field=models.CharField(default='tmp', max_length=10, unique=True),
            preserve_default=False,
        ),
    ]