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
import numpy as np
import accounting.helper_functions as hf

from bokeh.plotting import figure, output_file, show 
from bokeh.embed import components
from bokeh.models import ColumnDataSource, Legend
from bokeh.models.tools import HoverTool, WheelZoomTool, ResetTool, BoxZoomTool
from bokeh.palettes import Spectral
from bokeh.core.properties import value as bvalue
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


@login_required
def income_items_create_view(request):
    if request.method == 'POST':
        incomeitem_form = IncomeItemsUpdateForm(request.user, request.POST, request.FILES)
        incomecategory_form = IncomeCategoriesForm(request.POST)

        if incomeitem_form.is_valid():
            iform = incomeitem_form.save()
            calculate_salary(iform, type='create')
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
    paginate_by = 6

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calculate_salary(context['object'],type='update')
        return context

class IncomeItemsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = IncomeItems
    permission_required = 'accounting.can_see_all_financials'
    success_url = reverse_lazy('accounting:incomeitems_list')

### view for seeing daily incomes
from django.db.models.functions import TruncMonth
from django.db.models import Avg, Count, Min, Sum
from django.core.paginator import Paginator

def get_category_names(obj):
    categories = list(obj.objects.all().values('name'))
    categories = [item['name'] for item in categories]
    return categories


@login_required
def daily_income_aggregation_view(request):
    categories = get_category_names(CategoryType) 

    exp_cat = get_category_names(ExpenseCategories)

    dates = list(IncomeItems.objects.filter(instructor=request.user).order_by('date').values('date').distinct())
    dates = pd.unique([item['date'].strftime('%Y-%B') for item in dates])[::-1]

    paginator = Paginator(dates, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    month_filter = datetime.datetime.strptime(page_obj.object_list[0], '%Y-%B')
    begin_month = hf.first_day_of_month(month_filter)
    end_month = hf.last_day_of_month(month_filter)
    month_dates = pd.date_range(begin_month, end_month, freq='D')
    df_dates = pd.DataFrame({'date':month_dates})

    if request.user.has_perm('accounting.can_see_own_financials') and request.user.has_perm('accounting.can_see_all_financials'):
        income = IncomeItems.objects.filter(date__month=month_filter.month, date__year=month_filter.year).values('date', 'item__category_type__name', 'brut_amount')
    elif request.user.has_perm('accounting.can_see_own_financials'):
        income = IncomeItems.objects.filter(instructor=request.user, date__month=month_filter.month, date__year=month_filter.year).values('date', 'item__category_type__name', 'brut_amount')
    else:
        return render(request, 'error.html')
    
    df = pd.DataFrame(income)
    df.columns = ['brut_amount', 'date', 'category']
    df.date = pd.to_datetime(df.date)
    cat_name = pd.unique(df.category)                   
        
    month_filter = datetime.datetime.strptime(page_obj.object_list[0], '%Y-%B')
    begin_month = hf.first_day_of_month( month_filter)
    end_month = hf.last_day_of_month(month_filter)
    month_dates = pd.date_range(begin_month, end_month, freq='D')

    df_dates = pd.concat([pd.DataFrame({'date':month_dates, 'category':x}) for x in cat_name])

    df = df_dates.merge(df, on=['date','category'], how='outer')
    df.brut_amount = df.brut_amount.fillna(0)
    df_monthly=df.groupby(['date','category'],as_index=False).sum()
    
    income_monthly = pd.pivot_table(df_monthly, index='category', columns='date', values='brut_amount', aggfunc='sum')
    
    month_names = income_monthly.columns
    stack_category = list(income_monthly.T.columns)
    x_axis = [x.strftime('%d') for x in income_monthly.columns]
    colors = ["#b7ded2", "#f6a6b2", "#f7c297", "#ffecb8", "#90d2d8", "#91a16a", "#b36154", "#738986", "#ddc173", "#8e8680"][:len(stack_category)]
    title = f'Daily income in {page_obj.object_list[0]}'

    script, div = plot_stacked_area(income_monthly.T, stack_category, x_axis, colors, title=title)
    
    income_monthly.columns = [x.strftime('%Y-%b-%d') for x in income_monthly.columns]
    income_monthly['Total'] = income_monthly.sum(axis=1)
    income_monthly.loc['Total']=income_monthly.sum()
    
    col_header = income_monthly.T.columns.values
    context = {
        'incomeitems_list':income_monthly.to_dict(),
        'col_header': col_header,
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
    categories = get_category_names(CategoryType) 

    exp_cat = get_category_names(ExpenseCategories)

    dates = list(IncomeItems.objects.filter(instructor=request.user).order_by('date').values('date').distinct())
    dates = pd.unique([item['date'].strftime('%Y') for item in dates])[::-1]

    paginator = Paginator(dates, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    month_filter = datetime.datetime.strptime(page_obj.object_list[0], '%Y')
    begin_month = hf.first_day_of_month(month_filter)
    end_month = month_filter.replace(month=12).replace(day=31)
    month_dates = pd.date_range(begin_month, end_month, freq='M')


    if request.user.has_perm('accounting.can_see_own_financials') and request.user.has_perm('accounting.can_see_all_financials'):
        income = IncomeItems.objects.filter(date__year=month_filter.year).values('date', 'item__category_type__name', 'brut_amount')
    elif request.user.has_perm('accounting.can_see_own_financials'):
        income = IncomeItems.objects.filter(instructor=request.user,  date__year=month_filter.year).values('date', 'item__category_type__name', 'brut_amount')
    else:
        return render(request, 'error.html')
    
    df = pd.DataFrame(income)
    df.columns = ['brut_amount', 'date', 'category']
    df.date = pd.to_datetime(df.date)
    cat_name = pd.unique(df.category)                   
        
    df_dates = pd.concat([pd.DataFrame({'date':month_dates, 'category':x}) for x in cat_name])

    df = df_dates.merge(df, on=['date','category'], how='outer')
    df.brut_amount = df.brut_amount.fillna(0)
    df['date'] = [x.strftime('%B') for x in df['date']]
    
    df_monthly=df.groupby(['date','category'],sort=False,as_index=False).sum()

    income_monthly = pd.pivot_table(df_monthly, index='category', columns='date', values='brut_amount', aggfunc='sum')
    

    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    income_monthly = income_monthly[month_names]

    stack_category = list(income_monthly.T.columns)
    x_axis = month_names#[x.strftime('%b') for x in income_monthly.columns]
    colors = ["#b7ded2", "#f6a6b2", "#f7c297", "#ffecb8", "#90d2d8", "#91a16a", "#b36154", "#738986", "#ddc173", "#8e8680"][:len(stack_category)]
    title = f'Monthly income in {page_obj.object_list[0]}'

    script, div = plot_stacked_area(income_monthly.T, stack_category, x_axis, colors, title=title)
    
    # income_monthly.columns = [x.strftime('%B') for x in income_monthly.columns]
    income_monthly['Total'] = income_monthly.sum(axis=1)
    income_monthly.loc['Total']=income_monthly.sum()
    
    col_header = income_monthly.T.columns.values
    context = {
        'incomeitems_list':income_monthly.to_dict(),
        'col_header': col_header,
        'page_obj':page_obj,
        'script' : script , 
        'div' : div,
    }



    return render(request, 'accounting/monthly_income_list.html', context)


### List, Create, update and delete salary distribution

class SalaryDistributionCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = SalaryDistribution
    permission_required = 'accounting.can_see_all_financials'
    fields = '__all__'
    success_url = reverse_lazy('accounting:salarydistribution_list')
    initial = {'bonus_type': 'R'}

    def get_initial(self):
        initial = super(SalaryDistributionCreate, self).get_initial()
        initial['instructor'] = self.request.user
        return initial

class SalaryDistributionListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = SalaryDistribution
    permission_required = 'accounting.can_see_all_financials'
    paginate_by = 10

class SalaryDistributionUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = SalaryDistribution
    permission_required = 'accounting.can_see_all_financials'
    fields = '__all__'

class SalaryDistributionDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = SalaryDistribution
    permission_required = 'accounting.can_see_all_financials'
    success_url = reverse_lazy('accounting:salarydistribution_list')


### List, Create, update and delete salary 


class SalaryListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Salary
    permission_required = 'accounting.can_see_own_financials'
    paginate_by = 10

    def get_queryset(self):
        u = self.request.user
        if u.has_perm('accounting.can_see_own_financials') and u.has_perm('accounting.can_see_all_financials'):
            return Salary.objects.all()
        else:
            return Salary.objects.filter(instructor=u)

class SalaryUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Salary
    permission_required = 'accounting.can_see_all_financials'
    fields = '__all__'

class SalaryDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Salary
    permission_required = 'accounting.can_see_all_financials'
    success_url = reverse_lazy('accounting:salary_list')

def calculate_salary(form, type='create'):
    date = form.date
    gym_owner = User.objects.get(username='zizi')
    instructor = form.instructor
    gr = instructor.groups.all()
    gr = [x.name for x in gr]
    item = form.item
    try:
        sb = SalaryDistribution.objects.get(instructor__username=instructor, item=item)
    except:
        sb = []
    if sb:
        if item.category_type.name == 'InfraShape':
            infra_owner = User.objects.get(username='diveki')
            sb_owner = SalaryDistribution.objects.get(instructor__username='diveki', item=item)
            if sb_owner.bonus_type == 'R':
                salary_owner = form.brut_amount * sb_owner.bonus
            elif sb_owner.bonus_type == 'F':
                salary_owner = sb_owner.bonus
            if type == 'create':
                save_salary(form, date, infra_owner, item, salary_owner)
            if type == 'update':    
                update_salary(form, date, infra_owner, item, salary_owner)
            # calculate the case when a trainer is involved
            if 'Employee' in gr:
                if sb.bonus_type == 'R':
                    salary_instructor = (form.brut_amount - salary_owner) * sb.bonus
                elif sb.bonus_type == 'F':
                    salary_instructor = sb.bonus
                if type == 'create':
                    save_salary(form, date, instructor, item, salary_instructor)
                if type == 'update':    
                    update_salary(form, date, instructor, item, salary_instructor)
                # the rest goes to the gym owner
                salary = form.brut_amount - salary_owner - salary_instructor
                if type == 'create':
                    save_salary(form, date, gym_owner, item, salary)
                if type == 'update':    
                    update_salary(form, date, gym_owner, item, salary)
            elif 'Employer' in gr:
                salary = form.brut_amount - salary_owner
                if type == 'create':
                    save_salary(form, date, instructor, item, salary)
                if type == 'update':    
                    update_salary(form, date, instructor, item, salary)
        # calculate salary for Speed Fitness
        if item.category_type.name == 'Speed Fitness':
            if 'Employee' in gr:
                if sb.bonus_type == 'R':
                    salary_instructor = (form.brut_amount - salary_owner) * sb.bonus
                elif sb.bonus_type == 'F':
                    salary_instructor = sb.bonus
                if type == 'create':
                    save_salary(form, date, instructor, item, salary_instructor)
                if type == 'update':    
                    update_salary(form, date, instructor, item, salary_instructor)
                # the rest goes to the gym owner
                salary = form.brut_amount  - salary_instructor
                if type == 'create':
                    save_salary(form, date, gym_owner, item, salary)
                if type == 'update':    
                    update_salary(form, date, gym_owner, item, salary)
            elif 'Employer' in gr:
                salary = form.brut_amount
                if type == 'create':
                    save_salary(form, date, instructor, item, salary)
                if type == 'update':    
                    update_salary(form, date, instructor, item, salary)
        # calculate salary for Speed Fitness
        if item.category_type.name == 'Herbalife':
            salary = form.brut_amount
            if type == 'create':
                save_salary(form, date, gym_owner, item, salary)
            if type == 'update':    
                update_salary(form, date, gym_owner, item, salary)
    else:
        if item.category_type.name == 'InfraShape':
            infra_owner = User.objects.get(username='diveki')
            sb_owner = SalaryDistribution.objects.get(instructor__username='diveki', item=item)
            if sb_owner.bonus_type == 'R':
                salary_owner = form.brut_amount * sb_owner.bonus
            elif sb_owner.bonus_type == 'F':
                salary_owner = sb_owner.bonus
            if type == 'create':
                save_salary(form, date, infra_owner, item, salary_owner)
            if type == 'update':    
                update_salary(form, date, infra_owner, item, salary_owner)

            salary = form.brut_amount - salary_owner
            if type == 'create':
                save_salary(form, date, gym_owner, item, salary)
            if type == 'update':    
                update_salary(form, date, gym_owner, item, salary)
        else:
            salary = form.brut_amount
            if type == 'create':
                save_salary(form, date, gym_owner, item, salary)
            if type == 'update':    
                update_salary(form, date, gym_owner, item, salary)


def save_salary(form, date, instructor, item, salary):
    sal = Salary.objects.create(
        date=date, 
        instructor = instructor,
        item = item,
        income_item = form,
        salary = salary
        )
    sal.save()

def update_salary(form, date, instructor, item, salary):
    print(form.id)
    sal = Salary.objects.get(instructor__username = instructor, income_item__id=form.id)
    sal.instructor=instructor
    sal.date=date
    sal.item=item
    sal.salary=salary
    sal.income_item=form
    sal.save()


# Monthly salary view
@login_required
def monthly_salary_view(request):
    categories = list(CategoryType.objects.all().values('name'))
    categories = [item['name'] for item in categories]

    exp_cat = list(ExpenseCategories.objects.all().values('name'))
    exp_cat = [item['name'] for item in exp_cat]

    dates = list(Salary.objects.filter(instructor=request.user).order_by('date').values('date').distinct())
    dates = pd.unique([item['date'].strftime('%Y') for item in dates])[::-1]
    if request.user.has_perm('accounting.can_see_own_financials') and request.user.has_perm('accounting.can_see_all_financials'):
        data=list(Salary.objects.annotate(month=TruncMonth('date')).values('month','instructor__first_name', 'instructor__last_name', 'salary'))
        data_expense=list(ExpenseItems.objects.annotate(month=TruncMonth('date')).values('month', 'item__name', 'item__category_type__name', 'brut_amount'))
    elif request.user.has_perm('accounting.can_see_own_financials'):
        data=list(Salary.objects.filter(instructor=request.user).annotate(month=TruncMonth('date')).values('month','instructor__first_name', 'instructor__last_name', 'salary'))
    else:
        return render(request, 'error.html')
    
    df = pd.DataFrame(data)
    df['name'] = df['instructor__first_name'] + ' ' + df['instructor__last_name']
    df = df.drop(columns=['instructor__first_name', 'instructor__last_name'])
    df.month = pd.to_datetime(df.month)
    names = pd.unique(df.name)                   
    
    df_expense = get_expense_df(data_expense)
    df_expense.month = pd.to_datetime(df_expense.month)

    paginator = Paginator(dates, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    month_filter = datetime.datetime.strptime(page_obj.object_list[0], '%Y')
    begin_month = month_filter
    end_month = month_filter.replace(month=12).replace(day=31)
    month_dates = pd.date_range(begin_month, end_month, freq='M')
    month_dates = [x.replace(day=1) for x in month_dates]

    df_dates = pd.concat([pd.DataFrame({'month':month_dates, 'name':x}) for x in names])

    df = df_dates.merge(df, on=['month','name'], how='outer')
    df.salary = df.salary.fillna(0)
    df_monthly=df.groupby(['name','month'],as_index=False).sum()
    income_monthly = pd.pivot_table(df_monthly, index='name', columns='month', values='salary', aggfunc='sum')
    income_monthly.columns = [datetime.datetime.strftime(x, '%B') for x in income_monthly.columns]
    income_monthly.loc['Total']=income_monthly.sum()
    income_monthly['Total'] = income_monthly.sum(axis=1)
    income_monthly['Average'] = income_monthly.loc[:,income_monthly.columns != 'Total'].mean(axis=1)

    df_dates_noname = pd.concat([pd.DataFrame({'month':month_dates, 'name':x}) for x in exp_cat])
    df_expense = df_dates_noname.merge(df_expense, on=['month', 'name'], how='outer')
    df_expense.expense = df_expense.expense.fillna(0)
    df_expense.category = df_expense.category.fillna(categories[0])
    exp_monthly=df_expense.groupby(['name','month'],as_index=False).sum()
    expense_monthly = pd.pivot_table(exp_monthly, index='name', columns='month', values='expense', aggfunc='sum')
    expense_monthly.columns = [datetime.datetime.strftime(x, '%B') for x in expense_monthly.columns]
    expense_monthly.loc['Total']=expense_monthly.sum()
    expense_monthly['Total'] = expense_monthly.sum(axis=1)
    expense_monthly['Average'] = expense_monthly.loc[:,expense_monthly.columns != 'Total'].mean(axis=1)

    month_names = list(income_monthly.T.index)[:-2]
    stack_category = list(income_monthly.T.columns)[:-1]
    x_axis = month_names
    colors = ["#b7ded2", "#f6a6b2", "#f7c297", "#ffecb8", "#90d2d8", "#91a16a", "#b36154", "#738986", "#ddc173", "#8e8680"][:len(stack_category)]
    title = f'Monthly Salary by People in {page_obj.object_list[0]}'
    
    script, div = plot_stacked_area(income_monthly.T, stack_category, x_axis, colors, title=title)

    stack_category = list(expense_monthly.T.columns)[:-1]
    x_axis = month_names
    colors = ["#b7ded2", "#f6a6b2", "#f7c297", "#ffecb8", "#90d2d8", "#91a16a", "#b36154", "#738986", "#ddc173", "#8e8680"][:len(stack_category)]
    title = f'Monthly Expense in {page_obj.object_list[0]}'
    
    script_exp, div_exp = plot_stacked_area(expense_monthly.T, stack_category, x_axis, colors, title=title)

    # net calculation
    month_names.append('Total')
    month_names.append('Average')
    net = pd.DataFrame(columns=month_names)
    net.loc['Income'] = income_monthly.loc['Total', :].values
    net.loc['Expense'] = expense_monthly.loc['Total', :].values
    net.loc['Net'] = net.loc['Income'] - net.loc['Expense']    

    x_axis = month_names[:-2]
    
    script_net, div_net = plot_line_with_bar(x_axis, net.loc['Net'].values[:-2], [net.loc['Income'].values, net.loc['Expense'].values], colors, names=['Net', 'Income', 'Expense'])

    context = {
        'incomeitems_list':income_monthly.T.to_dict(),
        'col_header':income_monthly.columns.values,
        'page_obj':page_obj,
        'script' : script , 
        'div' : div,
        'expenseitems':expense_monthly.T.to_dict(),
        'script_exp':script_exp,
        'div_exp' : div_exp,
        'script_net':script_net,
        'div_net' : div_net,
        'netincome':net.T.to_dict(),
    }

    return render(request, 'accounting/salary_vs_expenses.html', context)

def plot_line_with_bar(x_axis, bars, lines, colors, names):
    n = len(lines)
    
    p = figure(plot_width=600, plot_height=350)
    
    x = list(range(len(x_axis)))
    h = np.array(bars) + 0.003
    adj_h = h
    
    data = {'bar':h/2, 'x_axis':x, 'height':adj_h}
    tooltips = [(f'{names[0]}', '@height{0.00}')]
    
    for i in range(n):
        data[f'line{i}'] = list(lines[i])
        tooltips.append((f'{names[1+i]}', f'@line{i}'))
    
    p.rect(x='x_axis', y='bar', width=0.9, height='height', color=colors[0], source=data)

    for i in range(n):
        p.line(x='x_axis', y=f'line{i}', color=colors[1+i], line_width=2, source=data)
        p.circle(x='x_axis', y=f'line{i}', color=colors[1+i], size=10, source=data)

    p.left[0].formatter.use_scientific=False
    p.xaxis.ticker=x
    p.xaxis.major_label_overrides={key:value[:3] for key, value in zip(x, x_axis)}
    p.add_tools(HoverTool(tooltips=tooltips))

    script, div = components(p)
    return script, div


def plot_stacked_area(df, stack_category, x_axis, colors, title='', xaxis_type=''):
    data = {'x_axis':x_axis}
    for cat in stack_category:
        data[cat] = list(df[cat].values)

    if xaxis_type == 'datetime':
        p = figure(x_range=x_axis, plot_height=350, title=title,
           toolbar_location='below', 
           tools="pan,wheel_zoom,box_zoom,reset", 
           tooltips="$name - @x_axis: @$name", x_axis_type='datetime')
    else:
        p = figure(x_range=x_axis, plot_height=350, title=title,
           toolbar_location='below', 
           tools="pan,wheel_zoom,box_zoom,reset", 
           tooltips="$name @x_axis: @$name")

    renderers = p.vbar_stack(
        stack_category,
        x="x_axis",
        width = 0.9,
        color=colors,
        source=data,
        legend = [bvalue(x) for x in stack_category]
    )
    
    p.left[0].formatter.use_scientific=False

    p.add_tools(BoxZoomTool())
    p.add_tools(ResetTool())

    script, div = components(p)
    return script, div

def get_expense_df(data_expense):
    df = pd.DataFrame(data_expense)
    df.columns = ['expense', 'category', 'name', 'month']
    return df


### List, Create, update and delete Expense items

class ExpenseItemsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = ExpenseItems
    permission_required = ('accounting.can_see_all_financials')
    fields = '__all__'
    success_url = reverse_lazy('accounting:expenseitems_list')

    def get_initial(self):
        return {
            'instructor':self.request.user,
        }


class ExpenseItemsListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = ExpenseItems
    permission_required = ('accounting.can_see_all_financials')
    paginate_by = 10


class ExpenseItemsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = ExpenseItems
    permission_required = 'accounting.can_see_all_financials'
    fields = '__all__'


class ExpenseItemsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ExpenseItems
    permission_required = 'accounting.can_see_all_financials'
    success_url = reverse_lazy('accounting:expenseitems_list')
