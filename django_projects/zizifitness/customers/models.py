from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
# Create your models here.

class Address(models.Model):
    """Model representing an address."""
    line1 = models.CharField(max_length=200, help_text='Enter street address (e.g. Szentharomsag utca 77, 1. emelet, 3as lakas)', blank=True)
    line2 = models.CharField(max_length=200, blank = True)
    city = models.CharField(max_length=200, blank = False)
    zip_code = models.CharField(max_length=200, blank = False)
    country = models.CharField(max_length=200, blank = False)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.line1}, {self.line2}, {self.zip_code}, {self.city},  {self.country}'

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.ForeignKey('PhoneNumber', on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    slug = models.SlugField(null=False, unique=True)

    GENDER_MAP = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    gender = models.CharField(
        max_length=1,
        choices=GENDER_MAP,
        blank=True,
        default='F',
    )

    @property
    def first_name(self):
        name = self.user.get_full_name().split(' ')
        if len(name) > 1:
            return name[0]
        else:
            return ''
    @property
    def last_name(self):
        name = self.user.get_full_name().split(' ')
        if len(name) > 1:
            return name[1]
        else:
            return ''

    class Meta:
        ordering = ['user']
        permissions = (('can_see_customers', 'Show all customers'),('can_see_all_financials', 'Show all financials'), ('can_see_own_financials', 'Show own financials'), ('can_edit_payment', 'Can edit payment'),('can_see_any_calendar', 'Can see any calendar'), ('can_edit_bookings', 'Can edit bookings'),('can_place_orders', 'Can place orders'),)

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        # import pdb
        # pdb.set_trace()
        return reverse('customers:person-detail', args=[str(self.slug)])
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.user.get_full_name())
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.last_name} {self.first_name}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.person.save()


class PhoneNumber(models.Model):
    country_code = models.CharField(max_length = 5, help_text='e.g. 36', blank=True)
    phone_number = models.CharField(max_length=20, help_text='e.g. 25654136', blank=True)

    def __str__(self):
        return f'+{self.country_code}-{self.phone_number}'


class Customer(models.Model):
    pass

class Physical_Appearance(models.Model):
    weight = models.FloatField()
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chest = models.FloatField()
    biceps = models.FloatField()
    hip = models.FloatField()
    tigh = models.FloatField()
    
class Body_Analysis(models.Model):
    pass
