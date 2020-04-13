from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import TextInput

from .views import *
import datetime

class IncomeItemsUpdateForm(forms.ModelForm):

    class Meta:
        model = IncomeItems
        fields = '__all__'
        permission_required = ('accounting.can_see_own_financials')
        success_url = reverse_lazy('accounting:incomeitems_list')
        # widgets = {
        #     'client': TextInput()
        # }

    def __init__(self, user, *args, **kwargs):
        super(IncomeItemsUpdateForm, self).__init__(*args, **kwargs)
        self.fields['instructor'].initial = user


class IncomeCategoriesForm(forms.ModelForm):

    class Meta:
        model = IncomeCategories
        fields = '__all__'
        permission_required = ('accounting.can_see_own_financials')

