# Generated by Django 3.0.4 on 2020-03-29 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0008_remove_expenseitems_client'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='incomeitems',
            options={'ordering': ['-id', 'date', 'item'], 'permissions': (('can_see_all_financials', 'Show all financials'), ('can_see_own_financials', 'Show own financials'))},
        ),
    ]
