from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import datetime

CATEGORY_CHOICES = (
    ('miss','MISSINGS'),
    ('crime', 'CRIMINALS'),
    ('mart','MARTYR'),
)
FILTER_CHOICES = (
    ('miss','MISSINGS'),
    ('crime', 'CRIMINALS'),
    ('mart','MARTYR'),
)

class ImageUploader(models.Model):
    
    title = models.CharField(max_length=200, unique=True, default='Untitled')
    photo = models.ImageField(upload_to="images")
    date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=7, choices=CATEGORY_CHOICES, default='home')
    filter = models.CharField(max_length=7, choices=FILTER_CHOICES, default='all')
    def save(self, *args, **kwargs):
        self.title = self.photo.name
        self.date = datetime.datetime.now()

        return super().save(*args, **kwargs)