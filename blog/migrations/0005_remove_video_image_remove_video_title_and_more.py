# Generated by Django 4.1.1 on 2022-09-29 12:40

from django.db import migrations
import django.utils.timezone
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='image',
        ),
        migrations.RemoveField(
            model_name='video',
            name='title',
        ),
        migrations.RemoveField(
            model_name='video',
            name='url',
        ),
        migrations.AddField(
            model_name='video',
            name='video',
            field=embed_video.fields.EmbedVideoField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]