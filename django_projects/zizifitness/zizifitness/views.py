from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

import datetime

from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


# Create your views here.
def index(request):

    context = {
        'hello': 'Zsolt',
        'title': 'Zizi Fitness',
    }

    return render(request, 'index.html', context=context)

#########################################
### FORMS
#########################################

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import *
from customers.views import *

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            # record date of birth
            user.person.date_of_birth = form.cleaned_data.get('date_of_birth')
            # record gender
            user.person.gender = form.cleaned_data.get('gender')
            # record address
            adr = Address.objects.create(
                line1 = form.cleaned_data.get('address_line1'),
                city = form.cleaned_data.get('address_city'),
                zip_code = form.cleaned_data.get('address_post_code'),
                country = form.cleaned_data.get('address_country'))
            user.person.address = adr
            #record phone number
            ph = PhoneNumber.objects.create(
                country_code = form.cleaned_data.get('phone_country'),
                phone_number = form.cleaned_data.get('phone_number')
            )
            user.person.phone_number = ph
            user.save()
            #sign new user in
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            # redirect the new user to its profile
            return redirect(user.person.get_absolute_url()) 
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# the decorator: To access the profile page, users should login
@login_required
def profile(request, **kwargs):
    if request.user.person.slug == kwargs.get('slug'):
        if request.method == 'POST':
            user_form = UserUpdateForm(request.POST, instance=request.user)
            person_form = PersonUpdateForm(request.POST, instance=request.user.person)

            if user_form.is_valid() and person_form.is_valid():
                user = user_form.save()
                # person_form.save()
                print('I am here')

                user.refresh_from_db()  # load the profile instance created by the signal
                # record date of birth
                user.person.date_of_birth = person_form.cleaned_data.get('date_of_birth')
                # record gender
                user.person.gender = person_form.cleaned_data.get('gender')
                # record address
                adr = Address.objects.create(
                    line1 = person_form.cleaned_data.get('address_line1'),
                    city = person_form.cleaned_data.get('address_city'),
                    zip_code = person_form.cleaned_data.get('address_post_code'),
                    country = person_form.cleaned_data.get('address_country'))
                user.person.address = adr
                #record phone number
                ph = PhoneNumber.objects.create(
                    country_code = person_form.cleaned_data.get('phone_country'),
                    phone_number = person_form.cleaned_data.get('phonenumber')
                )
                user.person.phone_number = ph
                user.save()
                messages.success(request, f'Your account has been updated!')
                return redirect(request.user.person.get_absolute_url())

        else:
            user_form = UserUpdateForm(instance=request.user)
            person_form = PersonUpdateForm(instance=request.user.person)

        context = {
            'u_form': user_form,
            'p_form': person_form
        }

        return render(request, 'registration/edit_profile.html', context)
    else:
        return HttpResponse("You do not have the permission to see the requested page.")

def error_html(request):
    return render(request, 'error.html')