

# videos/serializers.py
from rest_framework import serializers
from .models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Video
        fields = "__all__"      # enthält video_file automatisch
        extra_kwargs = {
            "url":        {"required": False, "allow_blank": True},
            "video_file": {"required": False, "allow_null": True},
        }

    def validate(self, data):
        # Mindestens EINES von beiden muss angegeben sein
        if not data.get("url") and not data.get("video_file"):
            raise serializers.ValidationError(
                "Bitte entweder 'url' ODER 'video_file' angeben."
            )
        return data
