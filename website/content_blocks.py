from wagtail import blocks
from coderedcms.blocks.content_blocks import *
from .collections_blocks import CONTENT_STREAMBLOCKS, HTML_STREAMBLOCKS, NAVIGATION_STREAMBLOCKS

class CustomAttributeWrapper(blocks.StructBlock):
    wrapper_tag = blocks.ChoiceBlock(
        choices=[
            ("div", "div"),
            ("section", "section"),
            ("article", "article"),
            ("aside", "aside"),
            ("span", "span"),
        ],
        default="div",
        label="Wrapper HTML Tag",
        help_text="Chọn thẻ HTML bao quanh nội dung"
    )

    custom_attribute = blocks.CharBlock(
        required=False,
        label="Custom attributes",
        help_text='Ví dụ: class="my-class" id="abc" data-x="1"'
    )

    content = blocks.StreamBlock(
        HTML_STREAMBLOCKS + CONTENT_STREAMBLOCKS + NAVIGATION_STREAMBLOCKS,
        required=True
    )

    class Meta:
        icon = "placeholder"
        template = "blocks/custom_attribute_wrapper.html"
        label = "Wrapper custom attribute"

