import os
from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from PIL import Image,ImageOps
# from api.images import make_thumbnail

# Create your models here.

class CustomUser(AbstractUser):
    name = models.CharField(max_length=250)



def user_directory_path(instance,filename):
    return 'images/{0}'.format(filename)


class Images(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    images = models.ImageField(upload_to = user_directory_path)
    thumbnail = models.ImageField(upload_to='', editable=False)
    # grayscale = models.ImageField(upload_to='', editable=False)
    slug = models.SlugField(max_length=250,unique_for_date='created_at')
    uploader = models.ForeignKey(CustomUser,on_delete=models.PROTECT,related_name='uploader')
    created_at = models.DateTimeField(default=timezone.now)


class imagevariations(models.Model):
    image = models.ForeignKey(Images,on_delete=models.CASCADE)
    grayscale = models.FileField()
    thumbnail = models.FileField(null=True)


class imagevariationssizes(models.Model):
    image = models.ForeignKey(Images,on_delete=models.CASCADE)
    sized_image = models.FileField(null=True)
