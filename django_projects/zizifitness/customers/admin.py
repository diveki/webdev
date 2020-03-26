from django.contrib import admin
from .models import Address, Person, PhoneNumber, Physical_Appearance, Body_Analysis

# Register your models here.

# class BooksInline(admin.TabularInline):
#     model = Book
#     extra = 0

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_name', 'first_name', 'date_of_birth', 'gender','address', 'phone_number')
    fields = ['user', 'date_of_birth', 'gender','phone_number', 'address', 'slug']
    # inlines = [BooksInline]


@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('country_code', 'phone_number')
    fields = ['country_code', 'phone_number']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('city', 'zip_code', 'country')
#     inlines = [BookInstanceInline]

@admin.register(Physical_Appearance)
class Physical_AppearanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'weight')
    fields = ['user', 'date', 'weight', 'chest', 'tigh', 'hip', 'biceps']

# admin.site.register(Author, AuthorAdmin)
# admin.site.register(Genre)
# #admin.site.register(BookInstance)
