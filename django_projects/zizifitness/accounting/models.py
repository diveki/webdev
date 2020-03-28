from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

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
        permissions = (('can_see_all_financials', 'Show all financials'), ('can_see_own_financials', 'Show own financials'))

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.category_type}: {self.name}'


class ExpenseCategories(models.Model):
    """Model representing a category type."""
    name = models.CharField(max_length=200, help_text='Enter a category name', blank=False)
    category_type = models.ForeignKey(CategoryType, on_delete=models.CASCADE, blank=False)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, blank=False, default=Decimal('0.0000'))
    currency = models.CharField(max_length=3, help_text='Enter a currency code',  blank=False, default='RSD')

    class Meta:
        permissions = (('can_see_all_financials', 'Show all financials'), ('can_see_own_financials', 'Show own financials'))

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.category_type}: {self.name}'


class IncomeItems(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True, default=datetime.date.today())
    item = models.ForeignKey(IncomeCategories, on_delete=models.CASCADE)
    net_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=False, default=Decimal('0.0000'))
    vat = models.DecimalField(max_digits=3, decimal_places=2, blank=False, default=Decimal('0.00'))
    brut_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=False, default=Decimal('0.0000'))

    class Meta:
        permissions = (('can_see_all_financials', 'Show all financials'), ('can_see_own_financials', 'Show own financials'))
    
    def __str__(self):
        return f'Income Item {self.item.name}'


class ExpenseItems(models.Model):
    client = models.OneToOneField(User, on_delete=models.CASCADE, related_name='%(app_label)s_%(class)s_related')
    instructor = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True, default=datetime.date.today())
    item = models.ForeignKey(ExpenseCategories, on_delete=models.CASCADE)
    net_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=False, default=Decimal('0.0000'))
    vat = models.DecimalField(max_digits=3, decimal_places=2, blank=False, default=Decimal('0.00'))
    brut_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=False, default=Decimal('0.0000'))

    class Meta:
        permissions = (('can_see_all_financials', 'Show all financials'), ('can_see_own_financials', 'Show own financials'))
    
    def __str__(self):
        return f'Expense Item {self.item.name}'
