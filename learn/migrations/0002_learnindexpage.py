# Generated by Django 5.0.4 on 2024-05-03 10:15

import django.db.models.deletion
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0001_initial'),
        ('wagtailcore', '0091_remove_revision_submitted_for_moderation'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearnIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('content', wagtail.fields.StreamField([('richtext', wagtail.blocks.RichTextBlock()), ('htmltext', wagtail.blocks.RawHTMLBlock()), ('imagetext', wagtail.blocks.StructBlock([('reverse', wagtail.blocks.BooleanBlock(help_text='Image on left? Defaults to right.', required=False)), ('text', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('caption', wagtail.blocks.BooleanBlock(required=False)), ('third', wagtail.blocks.BooleanBlock(help_text='1:2 split? Default is 1:1', required=False))]))])),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]