from wagtail.blocks import StructBlock, StreamBlock
from wagtail import blocks
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.images.blocks import ImageChooserBlock


class ImageText(StructBlock):
    reverse = blocks.BooleanBlock(help_text='Image on left? Defaults to right.', required=False)
    text = blocks.RichTextBlock()
    image = ImageChooserBlock()
    caption = blocks.BooleanBlock(required=False)
    third = blocks.BooleanBlock(help_text="1:2 split? Default is 1:1", required=False)

class YouTubeBlock(StructBlock):
    video_id = blocks.CharBlock()
    caption = blocks.CharBlock(required=False)

class BodyBlock(StreamBlock):
    richtext = blocks.RichTextBlock()
    htmltext = blocks.RawHTMLBlock()
    table =  TableBlock(template="partials/table_template.html")
    imagetext = ImageText()
    youtube = YouTubeBlock(template="partials/youtube_template.html")