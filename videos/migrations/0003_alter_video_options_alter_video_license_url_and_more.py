# Generated by Django 5.2 on 2025-05-13 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_remove_video_url_video_category_video_description_de_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterField(
            model_name='video',
            name='license_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='source_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
