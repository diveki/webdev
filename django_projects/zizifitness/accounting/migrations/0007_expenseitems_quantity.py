# Generated by Django 3.0.4 on 2020-03-29 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0006_auto_20200329_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenseitems',
            name='quantity',
            field=models.IntegerField(default='0'),
        ),
    ]
