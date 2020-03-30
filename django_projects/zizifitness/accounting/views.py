from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required

from .models import *
from .forms import *
import decimal
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

### List, Create, update and delete income categories

class IncomeCategoriesCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = IncomeCategories
    permission_required = 'accounting.can_see_all_financials'
    fields = '__all__'
    success_url = reverse_lazy('accounting:incomecategories_list')
    # initial = {'date_of_death': '05/01/2018'}

class IncomeCategoriesListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = IncomeCategories
    permission_required = 'accounting.can_see_all_financials'
    paginate_by = 10

class IncomeCategoriesUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = IncomeCategories
    permission_required = 'accounting.can_see_all_financials'
    fields = '__all__'

class IncomeCategoriesDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = IncomeCategories
    permission_required = 'accounting.can_see_all_financials'
    success_url = reverse_lazy('accounting:incomecategories_list')

### List, Create, update and delete Expense categories

class ExpenseCategoriesCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ExpenseCategories
    permission_required = 'accounting.can_see_all_financials'
    fields = '__all__'
    success_url = reverse_lazy('accounting:expensecategories_list')
    # initial = {'date_of_death': '05/01/2018'}

class ExpenseCategoriesListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = ExpenseCategories
    permission_required = 'accounting.can_see_all_financials'
    paginate_by = 10

class ExpenseCategoriesUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ExpenseCategories
    permission_required = 'accounting.can_see_all_financials'
    fields = '__all__'

class ExpenseCategoriesDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ExpenseCategories
    permission_required = 'accounting.can_see_all_financials'
    success_url = reverse_lazy('accounting:expensecategories_list')


### List, Create, update and delete Expense categories

# class IncomeItemsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
#     model = IncomeItems
#     permission_required = ('accounting.can_see_own_financials')
#     fields = '__all__'
#     success_url = reverse_lazy('accounting:incomeitems_list')

#     def get_initial(self):
#         initial = super(IncomeItemsCreate, self).get_initial()
#         initial['instructor'] = self.request.user
#         return initial

@login_required
def income_items_create_view(request):
    if request.method == 'POST':
        incomeitem_form = IncomeItemsUpdateForm(request.user, request.POST, request.FILES)
        incomecategory_form = IncomeCategoriesForm(request.POST)

        if incomeitem_form.is_valid():
            incomeitem_form.save()
            return redirect('accounting:incomeitems_list')        

        else:
           context = {
                'incomeitem_form': incomeitem_form,
                'incomecategory_form': incomecategory_form,
            }

    else:
        context = {
            'incomeitem_form': IncomeItemsUpdateForm(user=request.user),
            'incomecategory_form': IncomeCategoriesForm(),
        }

    return render(request, 'accounting/incomeitems_create.html', context)


class IncomeItemsListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = IncomeItems
    permission_required = ('accounting.can_see_own_financials')
    paginate_by = 5

    def get_queryset(self):
        u = self.request.user
        if u.has_perm('accounting.can_see_own_financials') and u.has_perm('accounting.can_see_all_financials'):
            return IncomeItems.objects.all()
        else:
            return IncomeItems.objects.filter(instructor=u)

class IncomeItemsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = IncomeItems
    permission_required = 'accounting.can_see_all_financials'
    fields = '__all__'

class IncomeItemsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = IncomeItems
    permission_required = 'accounting.can_see_all_financials'
    success_url = reverse_lazy('accounting:incomeitems_list')

