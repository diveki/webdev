from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils.timezone import now as djnow

from decimal import Decimal
import datetime
# Create your models here.

class CategoryType(models.Model):
    """Model representing a category type."""
    name = models.CharField(max_length=200, help_text='Enter a category type', blank=False)

    class Meta:
        permissions = (('can_see_all_financials', 'Show all financials'), ('can_see_own_financials', 'Show own financials'))

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}'


class IncomeCategories(models.Model):
    """Model representing a category type."""
    name = models.CharField(max_length=200, help_text='Enter a category name', blank=False)
    category_type = models.ForeignKey(CategoryType, on_delete=models.CASCADE, blank=False)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, blank=False)
    currency = models.CharField(max_length=3, help_text='Enter a currency code', blank=False)

    class Meta:
        ordering = ['category_type']
        permissions = (('can_see_all_financials', 'Show all financials'), ('can_see_own_financials', 'Show own financials'))

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.category_type}: {self.name}: {self.unit_price},{self.currency}'


class ExpenseCategories(models.Model):
    """Model representing a category type."""
    name = models.CharField(max_length=200, help_text='Enter a category name', blank=False)
    category_type = models.ForeignKey(CategoryType, on_delete=models.CASCADE, blank=False)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, blank=False, default=Decimal('0.0000'))
    currency = models.CharField(max_length=3, help_text='Enter a currency code',  blank=False, default='RSD')

    class Meta:
        ordering = ['category_type']
        permissions = (('can_see_all_financials', 'Show all financials'), ('can_see_own_financials', 'Show own financials'))

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.category_type}: {self.name}: {self.unit_price},{self.currency}'


class IncomeItems(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True, default=djnow())
    item = models.ForeignKey(IncomeCategories, on_delete=models.CASCADE)
    quantity = models.IntegerField(default='0')
    net_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=False, default=Decimal('0.00'))
    vat = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=Decimal('0.00'))
    brut_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=False, default=Decimal('0.00'))

    class Meta:
        ordering = ['-id', 'date', 'item']
        permissions = (('can_see_all_financials', 'Show all financials'), ('can_see_own_financials', 'Show own financials'))

    def get_absolute_url(self):
        return reverse('accounting:incomeitems_update', kwargs={'pk': self.pk})
    
    def __str__(self):
        return f'Income Item {self.item.name}'


class ExpenseItems(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True, default=djnow())
    item = models.ForeignKey(ExpenseCategories, on_delete=models.CASCADE)
    quantity = models.IntegerField(default='0')
    net_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=False, default=Decimal('0.00'))
    vat = models.DecimalField(max_digits=3, decimal_places=2, blank=False, default=Decimal('0.00'))
    brut_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=False, default=Decimal('0.00'))

    class Meta:
        ordering = ['date', 'item']
        permissions = (('can_see_all_financials', 'Show all financials'), ('can_see_own_financials', 'Show own financials'))
    
    def __str__(self):
        return f'Expense Item {self.item.name}'


class SalaryDistribution(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(IncomeCategories, on_delete=models.CASCADE)
    bonus = models.DecimalField(max_digits=8, decimal_places=2, blank=False, default=Decimal('0.00'))
    
    bonus_type_map = (
        ('F','Fixed'),
        ('R','Ratio'),
    )
    bonus_type = models.CharField(
        max_length=1,
        choices=bonus_type_map,
        blank=False,
        default='F',
    )

    class Meta:
        ordering = ['instructor', 'item']
        
    def __str__(self):
        return f'{self.instructor.get_full_name()}, {self.item.name}, {self.item.category_type.name}, {self.bonus_type}, {self.bonus}'


class Salary(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=False, default=djnow())
    item = models.ForeignKey(IncomeCategories, on_delete=models.CASCADE)
    income_item = models.ForeignKey(IncomeItems, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=8, decimal_places=2, blank=False, default=Decimal('0.00'))

    class Meta:
        ordering = ['-id', 'date', 'instructor', 'item']

    def get_absolute_url(self):
        return reverse('salary', kwargs={'pk': self.pk})
    
    def __str__(self):
        return f'Salary {self.instructor.get_full_name()}, {self.date}, {self.item.name}, {self.salary}, IncomeItem_id: {self.income_item.id}'
