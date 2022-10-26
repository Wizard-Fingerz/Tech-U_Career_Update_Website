from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
from embed_video.fields import EmbedVideoField
# Create your models here.

    
class Faculty(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name



class Department(models.Model):
    name = models.CharField(max_length=200)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class Programme(models.Model):
    name = models.CharField(max_length=210, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete = models.CASCADE)
    header_image = models.URLField()
    url = models.URLField()
    site = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=datetime.now, blank=True)
    
   
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
    


class Video(models.Model):
    video = EmbedVideoField()
    department = models.ForeignKey(Department, on_delete = models.CASCADE)

