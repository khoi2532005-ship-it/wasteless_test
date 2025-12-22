

from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from coderedcms.blocks import *
from coderedcms.blocks.stream_form_blocks import *
from coderedcms.blocks.layout_blocks import *
from .content_blocks import CustomAttributeWrapper
# Collections of blocks commonly used together.

HTML_STREAMBLOCKS = [
    ("text", RichTextBlock(icon="cr-font")),
    ("button", ButtonBlock()),
    ("image", ImageBlock()),
    ("image_link", ImageLinkBlock()),
    (
        "html",
        blocks.RawHTMLBlock(
            icon="code",
            form_classname="monospace",
            label=_("HTML"),
        ),
    ),
    ("download", DownloadBlock()),
    ("embed_video", EmbedVideoBlock()),
    ("quote", QuoteBlock()),
    ("table", TableBlock()),
    ("google_map", EmbedGoogleMapBlock()),
    ("page_list", PageListBlock()),
    ("page_preview", PagePreviewBlock()),
]

CONTENT_STREAMBLOCKS = HTML_STREAMBLOCKS + [
    ("accordion", AccordionBlock()),
    ("card", CardBlock()),
    ("carousel", CarouselBlock()),
    ("film_strip", FilmStripBlock()),
    ("image_gallery", ImageGalleryBlock()),
    ("modal", ModalBlock(HTML_STREAMBLOCKS)),
    ("pricelist", PriceListBlock()),
    ("reusable_content", ReusableContentBlock()),
    ("wrapper", CustomAttributeWrapper()),
]

NAVIGATION_STREAMBLOCKS = [
    ("page_link", NavPageLinkWithSubLinkBlock()),
    ("external_link", NavExternalLinkWithSubLinkBlock()),
    ("document_link", NavDocumentLinkWithSubLinkBlock()),
]
LAYOUT_STREAMBLOCKS = [
    (
        "hero",
        HeroBlock(
            [
                ("row", GridBlock(CONTENT_STREAMBLOCKS)),
                (
                    "cardgrid",
                    CardGridBlock(
                        [
                            ("card", CardBlock()),
                        ]
                    ),
                ),
                (
                    "html",
                    blocks.RawHTMLBlock(
                        icon="code", form_classname="monospace", label=_("HTML")
                    ),
                ),
            ]
        ),
    ),
    ("row", GridBlock(CONTENT_STREAMBLOCKS)),
    (
        "cardgrid",
        CardGridBlock(
            [
                ("card", CardBlock()),
            ]
        ),
    ),
    (
        "html",
        blocks.RawHTMLBlock(
            icon="code", form_classname="monospace", label=_("HTML")
        ),
    ),
    ("wrapper", CustomAttributeWrapper()),
]

STREAMFORM_FIELDBLOCKS = [
    ("sf_singleline", CoderedStreamFormCharFieldBlock(group=_("Fields"))),
    ("sf_multiline", CoderedStreamFormTextFieldBlock(group=_("Fields"))),
    ("sf_number", CoderedStreamFormNumberFieldBlock(group=_("Fields"))),
    ("sf_checkboxes", CoderedStreamFormCheckboxesFieldBlock(group=_("Fields"))),
    ("sf_radios", CoderedStreamFormRadioButtonsFieldBlock(group=_("Fields"))),
    ("sf_dropdown", CoderedStreamFormDropdownFieldBlock(group=_("Fields"))),
    ("sf_checkbox", CoderedStreamFormCheckboxFieldBlock(group=_("Fields"))),
    ("sf_date", CoderedStreamFormDateFieldBlock(group=_("Fields"))),
    ("sf_time", CoderedStreamFormTimeFieldBlock(group=_("Fields"))),
    ("sf_datetime", CoderedStreamFormDateTimeFieldBlock(group=_("Fields"))),
    ("sf_image", CoderedStreamFormImageFieldBlock(group=_("Fields"))),
    ("sf_file", CoderedStreamFormFileFieldBlock(group=_("Fields"))),
]

STREAMFORM_BLOCKS = [
    (
        "step",
        CoderedStreamFormStepBlock(STREAMFORM_FIELDBLOCKS + HTML_STREAMBLOCKS),
    ),
]