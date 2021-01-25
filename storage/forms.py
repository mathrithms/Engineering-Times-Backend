from django.forms import ModelForm
from .models import Store

# Create the form class.


class StoreForm(ModelForm):
    class Meta:
        model = Store
        fields = ['file', ]
