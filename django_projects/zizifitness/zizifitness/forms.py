from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from customers.models import *


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='First Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    
    address_line1 = forms.CharField(max_length=100, help_text='Optional. e.g. Test street 42, 1. floor, 2. door', label = 'Street', required=False)
    address_city = forms.CharField(max_length=100, help_text='Optional. e.g. Szeged', label = 'City', required=False)
    address_post_code = forms.CharField(max_length=100, help_text='Optional. e.g. 6724', label = 'Post code', required=False)
    address_country = forms.CharField(max_length=100, help_text='Optional. e.g. Serbia', label = 'Country', required=False)
    phone_country = forms.CharField(max_length=5, help_text='Optional. e.g. 381', label = 'Country code', required=False)
    phone_number = forms.CharField(max_length=20, help_text='Optional. e.g. 20581734', label = 'Phone number', required=False)
    date_of_birth = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    # slug = models.SlugField(null=False, unique=True)

    GENDER_MAP = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    gender = forms.ChoiceField(
        choices=GENDER_MAP
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'date_of_birth', 'address_line1', 'address_city', 'address_post_code', 'address_country', 'phone_country', 'phone_number', 'gender')

# User update form allows users to update user name and email
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# Profile update form allows users to update image
class PersonUpdateForm(forms.ModelForm):
    address_line1 = forms.CharField(max_length=100, help_text='Optional. e.g. Test street 42, 1. floor, 2. door', label = 'Street', required=False)
    address_city = forms.CharField(max_length=100, help_text='Optional. e.g. Szeged', label = 'City', required=False)
    address_post_code = forms.CharField(max_length=100, help_text='Optional. e.g. 6724', label = 'Post code', required=False)
    address_country = forms.CharField(max_length=100, help_text='Optional. e.g. Serbia', label = 'Country', required=False)
    phone_country = forms.CharField(max_length=5, help_text='Optional. e.g. 381', label = 'Country code', required=False)
    phonenumber = forms.CharField(max_length=20, help_text='Optional. e.g. 20581734', label = 'Phone number', required=False)

    class Meta:
        model = Person
        fields = ['address_line1', 'address_city', 'address_post_code', 'address_country', 'phone_country', 'phonenumber', 'date_of_birth', 'gender']
    
    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('instance')
        super(PersonUpdateForm, self).__init__(*args, **kwargs)
        def check_if_nonetype(x, atr):
            print(x)
            if x is None:
                return ''
            else:
                return getattr(x, atr)

        self.fields['address_line1'].initial = check_if_nonetype(current_user.address, 'line1')
        self.fields['address_city'].initial = check_if_nonetype(current_user.address, 'city')
        self.fields['address_post_code'].initial = check_if_nonetype(current_user.address, 'zip_code')
        self.fields['address_country'].initial = check_if_nonetype(current_user.address, 'country')
        self.fields['phone_country'].initial = check_if_nonetype(current_user.phone_number, 'country_code')
        self.fields['phonenumber'].initial = check_if_nonetype(current_user.phone_number, 'phone_number')
        self.fields['date_of_birth'].initial = current_user.date_of_birth
        self.fields['gender'].initial = current_user.gender
        
