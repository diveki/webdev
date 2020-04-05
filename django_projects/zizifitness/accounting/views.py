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
import pandas as pd
import accounting.helper_functions as hf

from bokeh.plotting import figure, output_file, show 
from bokeh.embed import components
from bokeh.models import ColumnDataSource, Legend
from bokeh.models.tools import HoverTool, WheelZoomTool, ResetTool, BoxZoomTool
from bokeh.palettes import Spectral
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

### view for seeing daily incomes
from django.db.models.functions import TruncMonth
from django.db.models import Avg, Count, Min, Sum
from django.core.paginator import Paginator

@login_required
def daily_income_aggregation_view(request):
    dates = list(IncomeItems.objects.filter(instructor=request.user).order_by('date').values('date').distinct())
    dates = pd.unique([item['date'].strftime('%Y-%B') for item in dates])[::-1]

    paginator = Paginator(dates, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    cattypes = pd.DataFrame(list(CategoryType.objects.all().values()))
    catnames = pd.DataFrame(list(IncomeCategories.objects.all().values()))
    catnames = catnames.merge(cattypes, left_on='category_type_id', right_on='id', suffixes=('_catname', '_category_type'))
    catnames = catnames.drop(columns=['category_type_id', 'id_category_type'])
    
    month_filter = datetime.datetime.strptime(page_obj.object_list[0], '%Y-%B')
    begin_month = hf.first_day_of_month(month_filter)
    end_month = hf.last_day_of_month(month_filter)
    month_dates = pd.date_range(begin_month, end_month, freq='D')
    df_dates = pd.DataFrame({'date':month_dates})
    if request.user.has_perm('accounting.can_see_own_financials') and request.user.has_perm('accounting.can_see_all_financials'):
        income = IncomeItems.objects.filter(date__month=month_filter.month, date__year=month_filter.year)
    elif request.user.has_perm('accounting.can_see_own_financials'):
        income = IncomeItems.objects.filter(instructor=request.user, date__month=month_filter.month, date__year=month_filter.year)
    else:
        return render(request, 'error.html')

    income_df = pd.DataFrame(list(income.values()))
    income_summary = calculate_daily_income_by_categories(income_df, catnames, cattypes, df_dates)

    script, div = plot_daily_income_per_month(income_summary, page_obj)

    context = {
        'incomeitems_list':income_summary.T.to_dict(),
        'col_header':income_summary.columns.values,
        'page_obj':page_obj,
        'script' : script , 
        'div' : div,
    }

    return render(request, 'accounting/daily_income_list.html', context)


def calculate_daily_income_by_categories(income, catnames, cattypes, df_dates):
    income = income.merge(catnames, left_on='item_id', right_on='id_catname')
    income = income.drop(columns=['id_catname', 'item_id', 'id', 'unit_price', 'vat', 'quantity'])
    income.brut_amount = income.brut_amount.apply(float)
    income_summary = income.groupby(['date','name_category_type'], as_index=False).sum()[['date', 'name_category_type', 'brut_amount']]
    income_summary.date = pd.to_datetime(income_summary.date)
    income_summary = df_dates.merge(income_summary, on='date', how='outer')
    income_summary.name_category_type = income_summary.name_category_type.fillna(cattypes.name[0])
    income_summary.brut_amount = income_summary.brut_amount.fillna(0)
    income_summary = pd.pivot_table(income_summary, values='brut_amount', index='date', columns='name_category_type', fill_value=0)
    income_summary['Total'] = income_summary.sum(axis=1)
    return income_summary

def plot_daily_income_per_month(income_summary, page_obj, freq='daily'):
    title = page_obj.object_list[0]
    colors = ["#c9d9d3", "#718dbf", "#e84d60"]
    stacks = list(income_summary.columns.drop('Total'))

    if freq == 'monthly':
        income_summary.index=[hf.first_day_of_month(x) for x in income_summary.index]
        income_summary.index = income_summary.index.rename('date')

    source = ColumnDataSource(income_summary)
    plot = figure(title=title, plot_width =500, plot_height =400, x_axis_type="datetime")

    renderers = plot.varea_stack(stacks,  x='date', source=source,color=colors[:len(stacks)], legend=[x+' ' for x in stacks])
    plot.legend.location = 'top_left'
    plot.left[0].formatter.use_scientific=False
        
    plot.add_tools(BoxZoomTool())
    plot.add_tools(ResetTool())
    hover = HoverTool(tooltips=[
        ('Date', '@date')
    ])
    plot.add_tools(hover)
    script, div = components(plot)
    return script, div


@login_required
def monthly_income_aggregation_view(request):
    dates = list(IncomeItems.objects.filter(instructor=request.user).order_by('date').values('date').distinct())
    dates = pd.unique([item['date'].strftime('%Y') for item in dates])[::-1]

    paginator = Paginator(dates, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    cattypes = pd.DataFrame(list(CategoryType.objects.all().values()))
    catnames = pd.DataFrame(list(IncomeCategories.objects.all().values()))
    catnames = catnames.merge(cattypes, left_on='category_type_id', right_on='id', suffixes=('_catname', '_category_type'))
    catnames = catnames.drop(columns=['category_type_id', 'id_category_type'])
    
    month_filter = datetime.datetime.strptime(page_obj.object_list[0], '%Y')
    begin_month = month_filter
    end_month = month_filter.replace(month=12).replace(day=31)
    month_dates = pd.date_range(begin_month, end_month, freq='D')
    df_dates = pd.DataFrame({'date':month_dates})
    if request.user.has_perm('accounting.can_see_own_financials') and request.user.has_perm('accounting.can_see_all_financials'):
        income = IncomeItems.objects.filter(date__year=month_filter.year)
    elif request.user.has_perm('accounting.can_see_own_financials'):
        income = IncomeItems.objects.filter(instructor=request.user,  date__year=month_filter.year)
    else:
        return render(request, 'error.html')

    income_df = pd.DataFrame(list(income.values()))
    income_summary = calculate_daily_income_by_categories(income_df, catnames, cattypes, df_dates)
    income_summary = income_summary.resample('M').sum()
    income_monthly = income_summary.T.copy()
    income_monthly.columns = [x.strftime('%B') for x in income_monthly.columns]
    income_monthly['Total'] = income_monthly.sum(axis=1)
    income_monthly['Average'] = income_monthly.mean(axis=1)

    script, div = plot_daily_income_per_month(income_summary, page_obj, freq='monthly')

    context = {
        'incomeitems_list':income_monthly.T.to_dict(),
        'col_header':income_monthly.columns.values,
        'page_obj':page_obj,
        'script' : script , 
        'div' : div,
    }

    return render(request, 'accounting/monthly_income_list.html', context)

