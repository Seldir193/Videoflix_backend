from modeltranslation.translator import register, TranslationOptions
from .models import Video


@register(Video)
class VideoTR(TranslationOptions):
    fields = ("title", "description")

