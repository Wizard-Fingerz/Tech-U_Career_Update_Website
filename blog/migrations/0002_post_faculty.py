# Generated by Django 4.1.1 on 2022-09-27 10:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='faculty',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blog.faculty'),
            preserve_default=False,
        ),
    ]
