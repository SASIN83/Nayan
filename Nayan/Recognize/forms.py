from django import forms
from Recognize.models import ImageUploader, CATEGORY_CHOICES


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageUploader
        fields = [
            "photo",
            "category",
        ]
        labels={'photo':''}


class FilterForm(forms.ModelForm):
    class Meta:
        model = ImageUploader
        fields = [
            "filter",
        ]