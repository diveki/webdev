from django.urls import path
from . import views

app_name = 'accounting'

urlpatterns = [
    path('', views.index, name='accounting'), 
    path('categorytype/create/', views.CategoryTypeCreate.as_view(), name='categorytype_create'), 
    path('categorytype/list/', views.CategoryTypeListView.as_view(), name='categorytype_list'),
    path('categorytype/<int:pk>/update', views.CategoryTypeUpdate.as_view(), name='categorytype_update'),
    path('categorytype/<int:pk>/delete/', views.CategoryTypeDelete.as_view(), name='categorytype_delete'),
]

## add incame categories path

urlpatterns += [
    path('incomecategories/create/', views.IncomeCategoriesCreate.as_view(), name='incomecategories_create'), 
    path('incomecategories/list/', views.IncomeCategoriesListView.as_view(), name='incomecategories_list'),
    path('incomecategories/<int:pk>/update', views.IncomeCategoriesUpdate.as_view(), name='incomecategories_update'),
    path('incomecategories/<int:pk>/delete/', views.IncomeCategoriesDelete.as_view(), name='incomecategories_delete'),
]

## add expense categories path

urlpatterns += [
    path('expensecategories/create/', views.ExpenseCategoriesCreate.as_view(), name='expensecategories_create'), 
    path('expensecategories/list/', views.ExpenseCategoriesListView.as_view(), name='expensecategories_list'),
    path('expensecategories/<int:pk>/update', views.ExpenseCategoriesUpdate.as_view(), name='expensecategories_update'),
    path('expensecategories/<int:pk>/delete/', views.ExpenseCategoriesDelete.as_view(), name='expensecategories_delete'),
]

## add income items path

urlpatterns += [
    # path('incomeitems/create/', views.IncomeItemsCreate.as_view(), name='incomeitems_create'),
    path('incomeitems/create/', views.income_items_create_view, name='incomeitems_create'), 
    path('incomeitems/list/', views.IncomeItemsListView.as_view(), name='incomeitems_list'),
    path('incomeitems/<int:pk>/update/', views.IncomeItemsUpdate.as_view(), name='incomeitems_update'),
    path('incomeitems/<int:pk>/delete/', views.IncomeItemsDelete.as_view(), name='incomeitems_delete'),
]

## add daily income list url

urlpatterns += [
    path('dailyincome/list/', views.daily_income_aggregation_view, name='daily_income'),
    path('monthlyincome/list/', views.monthly_income_aggregation_view, name='monthly_income'),
]

## add salary distribution path

urlpatterns += [
    path('salarydistribution/create/', views.SalaryDistributionCreate.as_view(), name='salarydistribution_create'), 
    path('salarydistribution/list/', views.SalaryDistributionListView.as_view(), name='salarydistribution_list'),
    path('salarydistribution/<int:pk>/update', views.SalaryDistributionUpdate.as_view(), name='salarydistribution_update'),
    path('salarydistribution/<int:pk>/delete/', views.SalaryDistributionDelete.as_view(), name='salarydistribution_delete'),
]

## add salary path

urlpatterns += [
    # path('salary/create/', views.SalaryCreate.as_view(), name='salary_create'), 
    path('salary/list/', views.SalaryListView.as_view(), name='salary_list'),
    path('salary/<int:pk>/update', views.SalaryUpdate.as_view(), name='salary_update'),
    path('salary/<int:pk>/delete/', views.SalaryDelete.as_view(), name='salary_delete'),
    path('salary/monthly/', views.monthly_salary_view, name='salary_monthly'),
]

## add expense items path

urlpatterns += [
    path('expenseitems/create/', views.ExpenseItemsCreate.as_view(), name='expenseitems_create'),
    path('expenseitems/list/', views.ExpenseItemsListView.as_view(), name='expenseitems_list'),
    path('expenseitems/<int:pk>/update/', views.ExpenseItemsUpdate.as_view(), name='expenseitems_update'),
    path('expenseitems/<int:pk>/delete/', views.ExpenseItemsDelete.as_view(), name='expenseitems_delete'),
]
