# Generated by Django 4.1.1 on 2022-09-26 14:36

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=210, null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.department')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('header_image', models.URLField()),
                ('url', models.URLField()),
                ('site', models.CharField(max_length=100)),
                ('content', models.TextField(blank=True, null=True)),
                ('date_posted', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.department')),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.faculty'),
        ),
    ]
