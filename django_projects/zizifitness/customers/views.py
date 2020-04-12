from django.shortcuts import render, redirect
from customers.models import *
from .forms import *
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

import datetime

from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
from django.core import serializers
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView

import pandas as pd
import numpy as np
import accounting.helper_functions as hf
import plot_functions as pf

from bokeh.plotting import figure, output_file, show 
from bokeh.embed import components
from bokeh.models import ColumnDataSource, Legend
from bokeh.models.tools import HoverTool, WheelZoomTool, ResetTool, BoxZoomTool
from bokeh.palettes import Spectral
from bokeh.core.properties import value as bvalue

# Create your views here.
def index(request):
 
    context = {
        'hello': 'Zsolt',
        'title': 'Zizi Fitness',
    }

    return render(request, 'customers/index.html', context=context)

def person_detail_view(request, **kwargs):
    # def format_object(x):
    #     tmp={}
    #     tmp['date']=x.date.strftime('%Y-%m-%d')
    #     tmp['weight']=x.weight
    #     return tmp
            
    person = get_object_or_404(Person, slug=kwargs.get('slug'))
    try:
        pa = Physical_Appearance.objects.filter(user__person__slug=kwargs.get('slug')).exclude(weight__isnull=True).order_by('-date').values('date', 'weight')
    except:
        return render(request, 'customers/person_detail.html', {'person':person})
    # if type(pa) == Physical_Appearance:
    #     data=format_object(pa)
    #     data = json.dumps(data)
    # else:
    #     struct = [format_object(x) for x in pa]
    #     data = json.dumps(struct)

    df = pd.DataFrame(list(pa))
    print(df)

    xaxis = list(df.date)
    y = [list(df.weight)]
    print(y)
    colors = ["#b7ded2", "#f6a6b2", "#f7c297", "#ffecb8", "#90d2d8", "#91a16a", "#b36154", "#738986", "#ddc173", "#8e8680"]
    title='Body weight'
    names = [['weight']]
    script, div = pf.plot_area_chart(xaxis, y, names, colors, title, xlabel='time', ylabel='Weight (kg)', xaxis_type='datetime')
    # month_names = income_monthly.columns
    # stack_category = list(income_monthly.T.columns)
    # x_axis = [x.strftime('%d') for x in income_monthly.columns]
    # colors = ["#b7ded2", "#f6a6b2", "#f7c297", "#ffecb8", "#90d2d8", "#91a16a", "#b36154", "#738986", "#ddc173", "#8e8680"][:len(stack_category)]
    # title = f'Daily income in {page_obj.object_list[0]}'

    # script, div = plot_stacked_area(income_monthly.T, stack_category, x_axis, colors, title=title)
    
    # income_monthly.columns = [x.strftime('%Y-%b-%d') for x in income_monthly.columns]
    # income_monthly['Total'] = income_monthly.sum(axis=1)
    # income_monthly.loc['Total']=income_monthly.sum()
    
    # col_header = income_monthly.T.columns.values


    return render(request, 'customers/person_detail.html', {'person':person, #'physical_appearance':data,
    'script' : script , 
    'div' : div,
})


class CustomersAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = Person
    permission_required = 'customers.can_see_customers'
    template_name = 'customers/customers_list_all.html'
    paginate_by = 20

    def get_queryset(self):
        return Person.objects.order_by('user')


# the decorator: To access the profile page, users should login
@login_required
def physical_appearance_updateview(request, **kwargs):
    if request.user.person.slug == kwargs.get('slug'):
        if request.method == 'POST':
            pa_form = Physical_AppearanceUpdateForm(request.POST, instance=request.user)
            if pa_form.is_valid():
                pa = Physical_Appearance.objects.create(
                    date=pa_form.cleaned_data.get('date'),
                    user=request.user,
                    weight=pa_form.cleaned_data.get('weight'),
                    chest=pa_form.cleaned_data.get('chest'),
                    biceps=pa_form.cleaned_data.get('biceps'),
                    hip=pa_form.cleaned_data.get('hip'),
                    tigh=pa_form.cleaned_data.get('tigh')
                )
                pa.save()
                messages.success(request, f'Your account has been updated!')
                return redirect(request.user.person.get_absolute_url())

        else:
            pa_form = Physical_AppearanceUpdateForm(instance=request.user)
            
        context = {
            'pa_form': pa_form
        }

        return render(request, 'customers/edit_measurements.html', context)
    else:
        return HttpResponse("You do not have the permission to see the requested page.")
