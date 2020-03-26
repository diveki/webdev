from django.shortcuts import render
from customers.models import *
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
from django.core import serializers

# Create your views here.
def index(request):
 
    context = {
        'hello': 'Zsolt',
        'title': 'Zizi Fitness',
    }

    return render(request, 'customers/index.html', context=context)

def person_detail_view(request, **kwargs):
    def format_object(x):
        tmp={}
        tmp['date']=x.date.strftime('%Y-%m-%d')
        tmp['weight']=x.weight
        return tmp
            
    person = get_object_or_404(Person, slug=kwargs.get('slug'))
    try:
        pa = Physical_Appearance.objects.filter(user__person__slug=kwargs.get('slug'))
    except:
        return render(request, 'customers/person_detail.html', {'person':person})
    if type(pa) == Physical_Appearance:
        data=format_object(pa)
        data = json.dumps(data)
    else:
        struct = [format_object(x) for x in pa]
        data = json.dumps(struct)

    return render(request, 'customers/person_detail.html', {'person':person, 'physical_appearance':data})

# class PersonDetailView(generic.DetailView):
#     model = Person
#     # slug_field = ''
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['physical_appearance'] = Physical_Appearance.objects.filter(user__username=self.object.user.username)
#         return context


class CustomersAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = Person
    permission_required = 'customers.can_see_customers'
    template_name = 'customers/customers_list_all.html'
    paginate_by = 20

    def get_queryset(self):
        return Person.objects.order_by('user')


