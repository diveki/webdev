from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import *
# Create your views here.

def index(request):
    if request.user.has_perm('customers.can_see_own_financials'):
        return render(request, 'accounting/index.html')
    else:
         return HttpResponse('Content of this link is not permitted!')

class CategoryTypeCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = CategoryType
    permission_required = 'accounting.can_see_all_financials'
    fields = '__all__'
    success_url = reverse_lazy('accounting:categorytype_list')
    # initial = {'date_of_death': '05/01/2018'}

class CategoryTypeListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = CategoryType
    permission_required = 'accounting.can_see_all_financials'
    paginate_by = 10

class CategoryTypeUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = CategoryType
    permission_required = 'accounting.can_see_all_financials'
    fields = '__all__'

class CategoryTypeDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = CategoryType
    permission_required = 'accounting.can_see_all_financials'
    success_url = reverse_lazy('accounting:categorytype_list')
