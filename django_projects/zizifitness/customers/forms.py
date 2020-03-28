from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .views import *
import datetime

class Physical_AppearanceUpdateForm(forms.ModelForm):

    class Meta:
        model = Physical_Appearance
        fields = ['date', 'weight', 'chest', 'biceps', 'hip', 'tigh']

    def __init__(self, *args, **kwargs):
        super(Physical_AppearanceUpdateForm, self).__init__(*args, **kwargs)
        self.fields['date'].initial = datetime.date.today().strftime('%Y-%m-%d')
        