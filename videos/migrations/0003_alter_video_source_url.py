# Generated by Django 5.2.1 on 2025-06-13 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_alter_video_category_alter_video_director_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='source_url',
            field=models.URLField(blank=True, editable=False, max_length=500, null=True),
        ),
    ]
