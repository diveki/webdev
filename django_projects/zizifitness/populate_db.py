from customers.models import *
from accounting.models import *
from django.contrib.auth.models import User, Group
from faker import Faker

def create_user(i):
    f = Faker()
    name = f.name().split(' ')
    user = User.objects.create_user(username=f'user{i}', password='Kistehen88', email=f.email(), first_name = name[0], last_name = name[1])
    user.save()
    return user

def create_address():
    # create address to user
    f = Faker()
    adr = f.address().split('\n')
    a = Address.objects.create(
        line1 = adr[0],
        city = f.city(),
        zip_code = f.postcode(),
        country = f.country())
    a.save()
    return a

def create_phone_number():
    f = Faker()
    cc = f.country_calling_code().strip().replace('+', '')
    ph = PhoneNumber.objects.create(
        country_code = cc,
        phone_number = f.msisdn()
    )
    ph.save()
    return ph

def create_person(n=50):
    f = Faker()
    for i in range(50):
        print(i)
        i=i+1
        user = create_user(i)
        adr = create_address()
        phone = create_phone_number()
        gr = create_client()
        gender = f.profile()['sex']
        dob = f.profile()['birthdate'].strftime('%Y-%m-%d')
        #create person
        user.person.address = adr
        user.person.phone_number = phone
        user.person.gender = gender
        user.person.date_of_birth = dob
        user.groups.add(gr)
        user.save()

def create_client():
    new_group, created = Group.objects.get_or_create(name='Customer')
    return new_group    

def create_employer_group():
    new_group, created = Group.objects.get_or_create(name='Employer')
    return new_group    

def create_superuser():
    user = User.objects.create_superuser(username=f'diveki', password='Kistehen88', email='diveki@gmail.com', first_name = 'Zsolt', last_name = 'Diveki')
    a = Address.objects.create(
        line1 = 'Damjanich utca 15A, 1/1',
        city = 'Szeged',
        zip_code = '6724',
        country = 'Hungary')
    ph = PhoneNumber.objects.create(
        country_code = '36',
        phone_number = '205658173'
    )
    dob = '1984-05-28'
    user.person.address = a
    user.person.phone_number = ph
    user.person.gender = 'M'
    user.person.date_of_birth = dob
    user.save()

def create_employer():
    user = User.objects.create_user(username=f'zizi', password='porcukornyuszi', email='hitrimo@gmail.com', first_name = 'Monika', last_name = 'Hitri')
    a = Address.objects.create(
        line1 = 'Majora Samardzica 9',
        city = 'Senta',
        zip_code = '24400',
        country = 'Serbia')
    ph = PhoneNumber.objects.create(
        country_code = '381',
        phone_number = '638343418'
    )
    dob = '1993-05-25'
    gr = create_employer_group()
    user.person.address = a
    user.person.phone_number = ph
    user.person.gender = 'F'
    user.person.date_of_birth = dob
    user.groups.add(gr)
    user.save()

def create_category_type():
    names = ['Speed Fitness', 'InfraShape', 'Herbalife']
    for nam in names:
        ph = CategoryType.objects.create(
            name = nam
        )
        ph.save()

def create_income_categories():
    name_map = {
        'Single Speed Fitness Training': ['Speed Fitness', 950, 'RSD'], 
        'Probe Speed Fitness': ['Speed Fitness', 500, 'RSD'],
        '9 Session Speed Fitness': ['Speed Fitness', 7200, 'RSD'],
        '4 Session Speed Fitness': ['Speed Fitness', 3400, 'RSD'],
        'Single Infrashape Horizontal': ['InfraShape', 1300, 'RSD'],
        'Probe Infrashape': ['InfraShape', 700, 'RSD'],
        '5 Session Infrashape': ['InfraShape', 6000, 'RSD'],
        '10 Session Infrashape': ['InfraShape', 11000, 'RSD'],
        'Herbalife shake SRB': ['Herbalife', 4000, 'RSD'],
        'Herbalife shake HUN': ['Herbalife', 4400, 'RSD'],
        'Herba protein csoki': ['Herbalife', 150, 'RSD'],
        'Herba tea': ['Herbalife', 2800, 'RSD'],
        'Rost tabletta': ['Herbalife', 2400, 'RSD'],
        'Herba maszk': ['Herbalife', 2000, 'RSD'],
    }
    
    for key, value in name_map.items():
        t=CategoryType.objects.get(name=value[0])
        ph = IncomeCategories.objects.create(
            name = key,
            category_type = t,
            unit_price = value[1],
            currency = value[2]
        )
        ph.save()

def create_expense_categories():
    name_map = {
        'Biotech feherje shake': 'Speed Fitness', 
        'Alsoruha': 'Speed Fitness',
        'Speedes rucik': 'Speed Fitness',
        'Folia nadrag': 'InfraShape',
        'Zsiregeto krem': 'InfraShape',
        'Herba tea': 'Herbalife',
        'Herba maszk': 'Herbalife',
        'Herba csomag': 'Herbalife',
        'Mosopor': 'Other',
        'Oblito': 'Other',
        'Tisztitoszer': 'Other',
        'Rezsi': 'Other',
        'Konyvelo': 'Other',
        'Sokolj': 'Other',
        'Szereles': 'Other',
    }
    
    for key, value in name_map.items():
        t=CategoryType.objects.get(name=value)
        ph = ExpenseCategories.objects.create(
            name = key,
            category_type = t
        )
        ph.save()


