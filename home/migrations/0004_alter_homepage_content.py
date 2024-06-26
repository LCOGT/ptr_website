# Generated by Django 5.0.6 on 2024-05-20 16:29

import wagtail.blocks
import wagtail.contrib.table_block.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_contentcategory_homepage_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='content',
            field=wagtail.fields.StreamField([('richtext', wagtail.blocks.RichTextBlock()), ('htmltext', wagtail.blocks.RawHTMLBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock(template='partials/table_template.html')), ('imagetext', wagtail.blocks.StructBlock([('reverse', wagtail.blocks.BooleanBlock(help_text='Image on left? Defaults to right.', required=False)), ('text', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.blocks.BooleanBlock(required=False)), ('third', wagtail.blocks.BooleanBlock(help_text='1:2 split? Default is 1:1', required=False))])), ('youtube', wagtail.blocks.StructBlock([('video_id', wagtail.blocks.CharBlock()), ('caption', wagtail.blocks.CharBlock(required=False))], template='partials/youtube_template.html'))]),
        ),
    ]
