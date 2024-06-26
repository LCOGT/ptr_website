# Generated by Django 5.0.4 on 2024-05-02 18:53

import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_create_homepage'),
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'content category',
                'verbose_name_plural': 'content categories',
            },
        ),
        migrations.AddField(
            model_name='homepage',
            name='content',
            field=wagtail.fields.StreamField([('richtext', wagtail.blocks.RichTextBlock()), ('htmltext', wagtail.blocks.RawHTMLBlock()), ('imagetext', wagtail.blocks.StructBlock([('reverse', wagtail.blocks.BooleanBlock(help_text='Image on left? Defaults to right.', required=False)), ('text', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.blocks.BooleanBlock(required=False)), ('third', wagtail.blocks.BooleanBlock(help_text='1:2 split? Default is 1:1', required=False))]))], default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homepage',
            name='featured_image',
            field=models.ForeignKey(blank=True, help_text='Homepage image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='summary',
            field=wagtail.fields.RichTextField(blank=True, verbose_name='optional summary/teaser'),
        ),
    ]
