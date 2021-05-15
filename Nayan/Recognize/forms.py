from django import forms
from Recognize.models import Image, CATEGORY_CHOICES


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = [
            "photo",
            "category",
        ]
        labels={'photo':''}


class FilterForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = [
            "filter",
        ]