from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import datetime
'''

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=25)
    slug = models.SlugField(null=False, unique=True)

    def get_absolute_url(self):
        return reverse('categories', args=[self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.title.replace(" ", "")
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
'''

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
    filter = models.CharField(max_length=7, choices=FILTER_CHOICES)

    '''
    def __str__(self):
        return str(self.id)
    '''

    def save(self, *args, **kwargs):
        self.title = self.photo.name
        self.date = datetime.datetime.now()

        return super().save(*args, **kwargs)