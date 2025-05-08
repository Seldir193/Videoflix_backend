from django.db import models


class Video(models.Model):
    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url         = models.URLField()
    created_at  = models.DateTimeField(auto_now_add=True)
    video_file = models.FileField(upload_to='videos' , blank=True, null=True)

    def __str__(self):
        return self.title
