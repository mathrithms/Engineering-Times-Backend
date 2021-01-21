from django import forms
from .models import Event


class ImageForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['image', ]
