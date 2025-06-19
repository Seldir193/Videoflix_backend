"""Modeltranslation configuration for the :class:`Video` model."""

from modeltranslation.translator import register, TranslationOptions
from .models import Video


@register(Video)
class VideoTR(TranslationOptions):
    """Translate *title* and *description* fields."""

    fields = ("title", "description")
