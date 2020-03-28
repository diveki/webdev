from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(CategoryType)
class CategoryTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    fields = ['name']

@admin.register(IncomeCategories)
class IncomeCategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'unit_price', 'currency')
    fields = ['name', 'category_type', 'unit_price', 'currency']

@admin.register(ExpenseCategories)
class ExpenseCategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'unit_price', 'currency')
    fields = ['name', 'category_type', 'unit_price', 'currency']


@admin.register(IncomeItems)
class IncomeItemsAdmin(admin.ModelAdmin):
    list_display = ('client', 'instructor', 'item', 'date', 'net_amount', 'vat', 'brut_amount')
    fields = ['client', 'instructor', 'item', 'date', 'net_amount', 'vat', 'brut_amount']

@admin.register(ExpenseItems)
class ExpenseItemsAdmin(admin.ModelAdmin):
    list_display = ('client', 'instructor', 'item', 'date', 'net_amount', 'vat', 'brut_amount')
    fields = ['client', 'instructor', 'item', 'date', 'net_amount', 'vat', 'brut_amount']
