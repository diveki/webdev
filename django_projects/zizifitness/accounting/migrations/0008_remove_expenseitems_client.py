# Generated by Django 3.0.4 on 2020-03-29 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0007_expenseitems_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expenseitems',
            name='client',
        ),
    ]