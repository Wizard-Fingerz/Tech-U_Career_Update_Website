from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from blog.models import *
from PIL import Image
from django.utils.timezone import now
from passlib.hash import pbkdf2_sha256
# Create your models here.




class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    department = models.ForeignKey(Department, on_delete= models.CASCADE)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, null=True)
    matric_number = models.CharField(max_length=20, null=True, unique=True)
    is_admin = models.BooleanField(default=False, verbose_name='Admin')
    is_student = models.BooleanField(default=False, verbose_name='Student')
    is_moderator = models.BooleanField(default=False, verbose_name='Student Moderator')
    
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        
    def __str__(self):
        return self.matric_number


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(default='default.jpg', upload_to ='profile_pics', blank = True, null = True)
    bio = models.TextField(blank=True, null=True)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
  
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
            
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    blog = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    dateTime = models.DateTimeField(default=now)
    
    def __str__(self) -> str:
        return self.user.username + "Comment: " + self.content