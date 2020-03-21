from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
from django.forms import ModelForm
from catalog.models import BookInstance, Book


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        
        # Check if a date is not in the past. 
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data


class CreateBookModelForm(ModelForm):
    def clean_isbn(self):
       data = self.data['isbn']
       print(data)
       # Check if a date is not in the past.
       if data:
           data = 'I was here'
       else:
           data = 'I was in else'
        #    raise ValidationError(_('ISBN code has to be 13 digits long'))

       # Remember to always return the cleaned data.
       return 'I was here'

    class Meta:
        model = Book
        fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
        # labels = {'due_back': _('Renewal date')}
        # help_texts = {'isbn': _('Enter a 13digit long code.')} 

