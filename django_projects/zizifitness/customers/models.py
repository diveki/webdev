from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances
# Create your models here.

class Address(models.Model):
    """Model representing an address."""
    line1 = models.CharField(max_length=200, help_text='Enter street address (e.g. Szentharomsag utca 77, 1. emelet, 3as lakas)', blank=True)
    line2 = models.CharField(max_length=200, blank = True)
    city = CharField(max_length=200, blank = False)
    zip_code = CharField(max_length=200, blank = False)
    country = CharField(max_length=200, blank = False)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.line1}, {self.line2}, {self.zip_code}, {self.city},  {self.country}'

class Person(models.Model):
    pass

class Customer(models.Model):
    pass

class Physical_Appearance(models.Model):
    pass

class Body_Analysis(models.Model):
    pass
